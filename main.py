from fastapi import FastAPI, Request, status
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# 使用你的 Channel Access Token 和 Channel Secret
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
# CHANNEL_ACCESS_TOKEN = "LoKrBjU0m+xx1bmPqTPaNE11fio8mtpnh0S0GEJrU5SChQKROYIh11vt1CFNszu7RcL/x6Cetvb5MLta+Ht1XOI8NLKTu7u1zq9i5s0dgbJShE3yT5fsQyjopyobw/SeAb7yZaF7iopXxaPTpdO5GwdB04t89/1O/w1cDnyilFU="
# CHANNEL_SECRET = "18aa4c8307b96d276ccf080475c7fe3b"
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
        TextSendMessage(text=event.message.text)  # 簡單地回覆相同訊息
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
