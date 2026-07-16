"""학습된 RAG 라우터 분류기를 학습에 없던 새 문장으로 확인하는 스모크 테스트.

사용법:
  python -m apps.ontology.training.test_rag_router
"""
from __future__ import annotations

from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_DIR = Path(__file__).parent.parent / "resources" / "rag_router" / "model"

# (문장, 사람이 기대하는 정답) — 학습 데이터(seed_dataset.jsonl)에 없던 새 표현들
TEST_CASES = [
    ("전북현대 감독이 누구야?", "rag_needed"),
    ("제주 유나이티드 코치진 정보 알려줘", "rag_needed"),
    ("K06팀 창단 연도랑 홈구장 같이 알려줘", "rag_needed"),
    ("이 선수 나이가 몇 살이야?", "rag_needed"),
    ("K리그 전체 팀 개수가 몇 개야?", "rag_needed"),
    ("비밀번호 재설정 링크를 다시 보내주세요", "auth"),
    ("휴대폰 인증이 안 돼요", "auth"),
    ("다른 사람이 내 계정에 로그인한 것 같아요", "auth"),
    ("탈퇴하려면 어디로 가야 해요?", "auth"),
    ("내 배송지 주소 변경하고 싶어요", "crud"),
    ("즐겨찾기 전체 삭제하고 싶어요", "crud"),
    ("너 오늘 기분 어때?", "general_qa"),
    ("손흥민 이번 시즌 골 몇 개야?", "general_qa"),  # 우리 DB엔 없는 EPL 정보
    ("축구공 크기 규격이 어떻게 돼?", "general_qa"),
]


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()

    correct = 0
    for text, expected in TEST_CASES:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=64)
        with torch.no_grad():
            logits = model(**inputs).logits
        pred_id = logits.argmax(dim=-1).item()
        pred_label = model.config.id2label[pred_id]
        prob = torch.softmax(logits, dim=-1)[0, pred_id].item()
        ok = pred_label == expected
        correct += ok
        mark = "O" if ok else "X"
        print(f"[{mark}] {text!r:45} 예측={pred_label:15} (p={prob:.2f})  기대={expected}")

    print(f"\n{correct}/{len(TEST_CASES)} 정답")


if __name__ == "__main__":
    main()
