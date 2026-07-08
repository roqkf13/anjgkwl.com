"""POST /chat — 프론트엔드 Gemini 채팅 연동."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.matrix.keymaker import generate_reply, get_gemini_model_name, is_gemini_configured

router = APIRouter(tags=["chat"])


class ChatMessage(BaseModel):
    role: str = Field(..., description="user | assistant")
    text: str = Field(..., min_length=1, max_length=32000)


class ChatRequest(BaseModel):
    """단일 message 또는 messages 배열(프론트 GeminiChat 호환)."""

    message: str | None = Field(default=None, max_length=32000)
    messages: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    text: str
    reply: str
    model: str


@router.post("/chat", response_model=ChatResponse)
def post_chat(req: ChatRequest):
    if not is_gemini_configured():
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY 가 설정되지 않았습니다. backend/.env 를 확인하세요.",
        )

    try:
        if req.messages:
            history = [m.model_dump() for m in req.messages]
            text = generate_reply(history=history)
        elif req.message and req.message.strip():
            text = generate_reply(message=req.message.strip())
        else:
            raise HTTPException(
                status_code=400,
                detail="message 또는 messages 중 하나는 필수입니다.",
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    model_name = get_gemini_model_name()
    return ChatResponse(text=text, reply=text, model=model_name)
