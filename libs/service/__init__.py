import uvicorn
from typing import Callable
from fastapi import FastAPI, Request, status
from starlette.responses import HTMLResponse
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from libs import configs
from libs.configs.logger import Logger
from libs.chatbot import ChatBot_Object


class Service(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._routes = []

    def route(self, path, **kwargs) -> Callable:
        def decorator(func):
            self._routes.append((path, func, kwargs))
            return func

        return decorator

    def register_default_actions(self) -> None:
        if configs.DEBUG:

            @self.get(configs.DOCS_URL, include_in_schema=False)
            def swagger_ui_html() -> HTMLResponse:
                return get_swagger_ui_html(
                    openapi_url=self.openapi_url,
                    title=f"{configs.SERVERTITLE} | Swagger UI",
                )

            @self.get(configs.REDOC_URL, include_in_schema=False)
            def redoc_ui_html() -> HTMLResponse:
                return get_redoc_html(
                    openapi_url=self.openapi_url,
                    title=f"{configs.SERVERTITLE} | ReDOC UI",
                )

        @self.on_event("startup")
        def startup_event():
            for log_name in configs.ACCESS_LOG_NAMES:
                Logger.setup_logger(log_name)

    def register_linebot_event_actions(self) -> None:
        @staticmethod
        @self.post("/webhook/", include_in_schema=False)
        async def callback(request: Request) -> dict:
            body = await request.body()
            signature = request.headers["X-Line-Signature"]
            try:
                configs.LINEBOT_HANDLER.handle(body.decode("utf-8"), signature)
            except InvalidSignatureError:
                return {
                    "error": "Invalid signature. Check your channel secret."
                }, status.HTTP_400_BAD_REQUEST

            return {"status": "OK"}

        @staticmethod
        @configs.LINEBOT_HANDLER.add(MessageEvent, message=TextMessage)
        def handle_message(event) -> None:
            """
            Line Bot processes Event text message logic segment.
            """
            user_text = event.message.text
            if user_text.startswith(configs.Start_Event_Text.question_keyword):
                response_text = ChatBot_Object.chat_completion(user_text)
                configs.LINEBOT_API.reply_message(
                    event.reply_token, TextSendMessage(text=response_text)
                )

    def service_run(self) -> None:
        self.register_default_actions()
        self.register_linebot_event_actions()

        uvicorn.run(self, host=configs.HOST, port=configs.PORT)
