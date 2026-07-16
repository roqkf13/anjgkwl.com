"""RAG 필요 여부 이진 분류기 학습 스크립트.

KLUE-RoBERTa 풀 파인튜닝. 양자화/PEFT/QLoRA 없음 — 110M급 인코더라 3050 8GB에서
그대로 fp32/fp16 학습 가능.

사용법:
  python -m apps.ontology.training.train_rag_router --overfit-check   # 먼저 소량으로 오버핏 검증
  python -m apps.ontology.training.train_rag_router                   # 전체 데이터 학습
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "klue/roberta-base"
DATA_PATH = Path(__file__).parent.parent / "resources" / "rag_router" / "seed_dataset.jsonl"
OUTPUT_DIR = Path(__file__).parent.parent / "resources" / "rag_router" / "model"

LABEL2ID = {"auth": 0, "crud": 1, "general_qa": 2, "rag_needed": 3}
ID2LABEL = {v: k for k, v in LABEL2ID.items()}


def load_examples(path: Path) -> list[tuple[str, int]]:
    examples: list[tuple[str, int]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            examples.append((row["text"], LABEL2ID[row["label"]]))
    return examples


class RagRouterDataset(Dataset):
    def __init__(self, examples: list[tuple[str, int]], tokenizer, max_length: int = 64) -> None:
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        text, label = self.examples[idx]
        enc = self.tokenizer(
            text, truncation=True, max_length=self.max_length, padding="max_length", return_tensors="pt"
        )
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long),
        }


def run_epoch(model, loader: DataLoader, optimizer, device: torch.device, train: bool) -> tuple[float, float]:
    model.train(train)
    total_loss, correct, count = 0.0, 0, 0
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        with torch.set_grad_enabled(train):
            out = model(**batch)
            loss = out.loss
        if train:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        batch_size = batch["labels"].size(0)
        total_loss += loss.item() * batch_size
        correct += (out.logits.argmax(dim=-1) == batch["labels"]).sum().item()
        count += batch_size
    return total_loss / count, correct / count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overfit-check", action="store_true",
        help="샘플 16개로 오버핏이 되는지만 확인 (모델 저장 안 함)",
    )
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")

    examples = load_examples(DATA_PATH)
    random.shuffle(examples)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=4, id2label=ID2LABEL, label2id=LABEL2ID
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)

    if args.overfit_check:
        subset = examples[:24]
        loader = DataLoader(RagRouterDataset(subset, tokenizer), batch_size=args.batch_size, shuffle=True)
        epochs = args.epochs or 30
        print(f"[오버핏 검증] 샘플 {len(subset)}개로 {epochs} epoch 학습 — loss가 0에 가까워지는지 확인")
        loss, acc = 0.0, 0.0
        for epoch in range(1, epochs + 1):
            loss, acc = run_epoch(model, loader, optimizer, device, train=True)
            print(f"  epoch {epoch:02d}  loss={loss:.4f}  acc={acc:.2%}")
        if loss < 0.05 and acc == 1.0:
            print("\n오버핏 성공 — 학습 루프가 정상 동작합니다. --overfit-check 없이 다시 실행하세요.")
        else:
            print("\n[경고] loss가 충분히 낮아지지 않았습니다 — 학습 루프나 데이터를 점검하세요.")
        return

    split = max(1, int(len(examples) * 0.8))
    train_examples, val_examples = examples[:split], examples[split:]
    train_loader = DataLoader(RagRouterDataset(train_examples, tokenizer), batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(RagRouterDataset(val_examples, tokenizer), batch_size=args.batch_size)

    epochs = args.epochs or 10
    best_val_acc = 0.0
    for epoch in range(1, epochs + 1):
        train_loss, train_acc = run_epoch(model, train_loader, optimizer, device, train=True)
        val_loss, val_acc = run_epoch(model, val_loader, optimizer, device, train=False)
        print(
            f"epoch {epoch:02d}  train_loss={train_loss:.4f} train_acc={train_acc:.2%}  "
            f"val_loss={val_loss:.4f} val_acc={val_acc:.2%}"
        )
        if val_acc >= best_val_acc:
            best_val_acc = val_acc
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(OUTPUT_DIR)
            tokenizer.save_pretrained(OUTPUT_DIR)

    print(f"\n학습 완료. best val_acc={best_val_acc:.2%}. 모델 저장 위치: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
