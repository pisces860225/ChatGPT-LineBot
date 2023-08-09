from linebot.models import MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status, HTTPException

from libs import configs
from libs.openAI import OpenAI_Object
from libs.chatbot import LineBot_Object
from libs.enumeration import StartEventTextKeywords


class ChatBot_Router:
    router = APIRouter()

    @staticmethod
    @router.post("/webhook/", include_in_schema=False)
    async def callback(request: Request) -> JSONResponse:
        body = await request.body()
        body_decoded = body.decode("utf-8")
        signature = request.headers.get("X-Line-Signature")
        if not signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Signature not found."
            )
        try:
            configs.LINEBOT_HANDLER.handle(body_decoded, signature)
        except InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature. Check your channel secret.",
            )

        return JSONResponse(content={"status": "OK"})

    @staticmethod
    @configs.LINEBOT_HANDLER.add(MessageEvent, message=TextMessage)
    def handle_text_message(event) -> None:
        """
        Line Bot processes Event text message logic segment.
        """
        user_text = event.message.text
        keyword, _, rest_of_text = user_text.partition(" ")
        match keyword:
            case StartEventTextKeywords.VERSION.value:
                response_text = f"{configs.SERVERTITLE} Version: v{configs.VERSION}\nOpenAI 使用的模型版本: {configs.OPENAI_USE_MODEL}"
                LineBot_Object.reply_text_to_user(event, response_text)

            case StartEventTextKeywords.QUESTION.value:
                response_text = OpenAI_Object.chat_completion(rest_of_text)
                LineBot_Object.reply_text_to_user(event, response_text)

            case StartEventTextKeywords.IMAGE_CREATOR.value:
                response_text = OpenAI_Object.image_completion(rest_of_text)
                if isinstance(response_text, str):
                    """
                    圖片參數錯誤，或 openai 回傳錯誤時將會返回一組錯誤敘述
                    """
                    LineBot_Object.reply_text_to_user(event, response_text)
                else:
                    LineBot_Object.reply_images_to_user(event, response_text)

            case _:
                pass