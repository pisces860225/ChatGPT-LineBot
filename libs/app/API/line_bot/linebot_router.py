import re
from linebot.models import MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status, HTTPException

from libs.configs import settings
from libs.openAI.openai_obj import OpenAI_Object
from libs.chatbot.chatbot_obj import LineBot_Object
from libs.enumeration import StartEventTextKeywords


class APIRouterClass:
    router = APIRouter()

    @staticmethod
    @router.post("/webhook/", include_in_schema=False)
    async def callback(request: Request) -> JSONResponse:
        """
        接收 Line Bot 的 Webhook 請求。
        """

        body = await request.body()
        body_decoded = body.decode("utf-8")
        signature = request.headers.get("X-Line-Signature")
        if not signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Signature not found."
            )
        try:
            settings.LINEBOT_HANDLER.handle(body_decoded, signature)
        except InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature. Check your channel secret.",
            )

        return JSONResponse(content={"status": "OK"})

    @staticmethod
    @settings.LINEBOT_HANDLER.add(MessageEvent, message=TextMessage)
    def handle_text_message(event) -> None:
        """
        LINE Bot 處理 Event 文字訊息的邏輯段。
        """
        user_text = event.message.text
        split_text = re.split(r"[ ,，]", user_text, maxsplit=1)
        keyword = split_text[0]
        rest_of_text = split_text[1] if len(split_text) > 1 else ""

        if keyword == StartEventTextKeywords.VERSION.value:
            """
            查看目前版本
            """
            response_text = f"{settings.SERVERTITLE} Version: v{settings.VERSION}\nOpenAI 使用的模型版本: {settings.OPENAI_USE_MODEL}"
            LineBot_Object.reply_text_to_user(event, response_text)

        elif keyword == StartEventTextKeywords.QUESTION.value:
            """
            文字生成器
            """
            response_text = OpenAI_Object.chat_completion(rest_of_text)
            LineBot_Object.reply_text_to_user(event, response_text)

        elif keyword == StartEventTextKeywords.CANDO_LIST.value:
            """
            能做的事情
            """
            response_text = "目前能做的指令分別為:\n\n"
            for index, enum_item in enumerate(StartEventTextKeywords):
                response_text += f"{index+1}. {enum_item.value}\n"
            LineBot_Object.reply_text_to_user(event, response_text)

        else:
            pass
