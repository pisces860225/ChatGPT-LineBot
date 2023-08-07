import uvicorn
from fastapi import FastAPI, Request, status
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from libs.chatbot import ChatGPT_Object
from libs import configs


class Service(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._routes = []

    def route(self, path, **kwargs):
        def decorator(func):
            self._routes.append((path, func, kwargs))
            return func

        return decorator

    def register_default_actions(self):
        if configs.DEBUG:

            @self.get(configs.DOCS_URL, include_in_schema=False)
            def swagger_ui_html():
                return get_swagger_ui_html(
                    openapi_url=self.openapi_url,
                    title=f"{configs.SERVERTITLE} | Swagger UI",
                )

            @self.get(configs.REDOC_URL, include_in_schema=False)
            def redoc_ui_html():
                return get_redoc_html(
                    openapi_url=self.openapi_url,
                    title=f"{configs.SERVERTITLE} | ReDOC UI",
                )

        @staticmethod
        @self.post("/webhook/")
        async def callback(request: Request):
            # 取得 request body
            body = await request.body()
            signature = request.headers["X-Line-Signature"]
            try:
                configs.LINEBOT_HANDLER.handle(body.decode("utf-8"), signature)
            except InvalidSignatureError:
                return {
                    "error": "Invalid signature. Check your channel secret."
                }, status.HTTP_400_BAD_REQUEST

            return "OK"

        @staticmethod
        @configs.LINEBOT_HANDLER.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            user_text = event.message.text
            if user_text.startswith("#秘書"):
                response_text = ChatGPT_Object.chat_completion(user_text)
                configs.LINEBOT_API.reply_message(
                    event.reply_token, TextSendMessage(text=response_text)
                )

    def service_run(self):
        self.register_default_actions()
        uvicorn.run(self, host=configs.HOST, port=configs.PORT)
