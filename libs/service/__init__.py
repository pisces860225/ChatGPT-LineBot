import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from libs import configs
from libs.configs.logger import Logger
from libs.chatbot.chatbot_router import ChatBot_Router


class Service(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
        self.include_router(ChatBot_Router.router, prefix="/chatbot")

    def service_run(self) -> None:
        self.register_default_actions()
        self.register_linebot_event_actions()

        uvicorn.run(self, host=configs.HOST, port=configs.PORT)
