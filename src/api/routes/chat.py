from fastapi import APIRouter,HTTPException,WebSocket
from openai import OpenAI
import os

router = APIRouter(
    tags=["Chat Routes"]
)

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")


client = OpenAI(api_key=API_KEY)


@router.websocket("/ws")
# websocket endpoint for streaming chat responses
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive the message from the client
        data = await websocket.receive_text()
        
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user","content": data}],
                stream=True,
            )
        except Exception as e:
            await websocket.send_text(str(e))
            raise HTTPException(status_code=500, detail=str(e))

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # Send the response to the client
                await websocket.send_text(str(chunk.choices[0].delta.content))
        
        # Send the end of the text to the client
        await websocket.send_text("<1230TextEnd1971>")

# endpoint for string responses
@router.websocket("/ws/simplified")
async def websocket_endpoint_simplified(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive the message from the client
        data = await websocket.receive_text()
        await websocket.send_text("your function goes here")
        await websocket.send_text("<1230TextEnd1971>")