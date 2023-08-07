from fastapi import FastAPI, Request, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.post("/webhook/")
async def callback(request: Request):
    # 取得 request body
    body = await request.body()
    signature = request.headers["X-Line-Signature"]

    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return {"error": "Invalid signature. Check your channel secret."}, status.HTTP_400_BAD_REQUEST

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
