from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.models import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.dependencies import get_chat_service
from app.auth.dependencies import get_current_user


router = APIRouter()


# =========================
# NORMAL CHAT
# =========================
@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    user: str = Depends(get_current_user)
):

    return service.process(
        request.session_id,
        request.message
    )


# =========================
# STREAM CHAT
# =========================
@router.post("/chat/stream")
def stream_chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    user: str = Depends(get_current_user)
):

    def generate():

        try:
            for token in service.stream_process(
                request.session_id,
                request.message
            ):
                yield token

        except Exception as e:
            print("STREAM ERROR:", e)
            yield "Stream failed."

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )