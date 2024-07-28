from fastapi import APIRouter,HTTPException,WebSocket
import openai
import os

router = APIRouter(
    tags=["Chat Routes"]
)

openai.api_key = os.getenv("OPENAI_API_KEY")
engine = os.getenv("MODEL")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=data,
            max_tokens=150,
            stream=True
        )
        for chunk in response:
            await websocket.send_text(chunk.choices[0].text.strip())