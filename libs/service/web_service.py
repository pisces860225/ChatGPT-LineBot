# -*- coding: utf-8 -*-
import uvicorn
import importlib
from pathlib import Path
from fastapi import FastAPI
from typing import Callable, Any, List
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from concurrent.futures import ThreadPoolExecutor
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from libs.configs import settings
from libs.logger.info_logger_handle import Logger
from libs.logger.access_logger_handle import AccessLogger


class Service(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._routes: list = []

    # ---------- 路由相關 ----------
    def route(
        self, path: str, **kwargs
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        重新定義路由裝飾器，並儲存路由資訊。

        args:
            path: 路由的路徑，例如: "/api/v1/test"
            **kwargs: 路由的其他參數，例如: methods=["GET", "POST"]

        return:
            decorator: 路由裝飾器
        """

        def decorator(func: Callable) -> Callable:
            self._routes.append((path, func, kwargs))
            return func

        return decorator

    # ---------- 模組導入相關 ----------
    def _get_all_module_files(self) -> List[Path]:
        """
        獲取所有 API 模組文件。

        return:
            List[Path]: 所有 API 模組文件
        """

        return [
            file
            for directory in settings.BASE_API_PATH.iterdir()
            if directory.is_dir()
            for file in directory.iterdir()
            if file.suffix == ".py" and not file.name.startswith("__")
        ]

    def _checker_and_import_API_modules(self) -> None:
        """
        動態註冊所有 API 模組。
        """

        Logger.debug("開始搜尋 API 資料夾並獲取 API 文件資訊。", color="blue")

        def import_and_register(module_file):
            module_name = f"{module_file.parent.name}.{module_file.stem}"

            should_register = (module_name in settings.API_ALLOW_LIST) or (
                settings.DEBUG and module_name in settings.DEBUG_API_ALLOW_LIST
            )

            if should_register:
                full_module_name = f"{settings.BASE_API_IMPORT_PATH}.{module_name}"
                imported_module = importlib.import_module(full_module_name)

                api_class = getattr(imported_module, "APIRouterClass", None)

                if api_class and hasattr(api_class, "router"):
                    self.include_router(api_class.router)
                    Logger.debug(f"{full_module_name}已經註冊。")

        # 使用 ThreadPoolExecutor 並行導入模組
        with ThreadPoolExecutor() as executor:
            list(executor.map(import_and_register, self._get_all_module_files()))

        Logger.debug("結束 API 資料夾搜索，已成功註冊所有 API。", color="blue")

    # ---------- 啟動和文檔相關 ----------
    def _get_documentation_ui_html(self, ui_type: str = "swagger") -> HTMLResponse:
        """
        生成 swagger 或 redoc 的 UI 文檔。

        args:
            ui_type: UI 的類型，可以是 swagger 或 redoc (default: swagger)

        return:
            HTMLResponse: UI 文檔的 HTMLResponse 物件
        """

        title = f"{settings.SERVERTITLE} | {ui_type.capitalize()} UI"
        return (
            get_swagger_ui_html(
                openapi_url=self.openapi_url,
                title=title,
            )
            if ui_type == "swagger"
            else get_redoc_html(
                openapi_url=self.openapi_url,
                title=title,
            )
        )

    def _startup_event(self) -> None:
        """
        FastAPI 啟動時的事件。
        """

        AccessLogger.setup_access_log_handler()

        Logger.debug(
            f"伺服器運行中"
            f"\nDEBUG MODE:    {settings.DEBUG}"
            f"\nRUN AS:        http://localhost:{settings.UVICORN_PORT}"
            f"\nSWAGGER URL:   http://localhost:{settings.UVICORN_PORT}{settings.DOCS_URL}"
            f"\nREDOC URL:     http://localhost:{settings.UVICORN_PORT}{settings.REDOC_URL}"
        )

    def _register_default_actions(self) -> None:
        """
        註冊預設的路由和重定義文檔 UI。
        """

        self.on_event("startup")(self._startup_event)

        if settings.DEBUG:
            self.get(settings.DOCS_URL, include_in_schema=False)(
                lambda: self._get_documentation_ui_html("swagger")
            )
            self.get(settings.REDOC_URL, include_in_schema=False)(
                lambda: self._get_documentation_ui_html("redoc")
            )

    # ---------- 啟動服務 ----------
    def _service_run(self) -> None:
        """
        進行 FastAPI 的初始化設定。
        """

        self._register_default_actions()

        for path, func, kwargs in self._routes:
            self.add_api_route(path, func, **kwargs)

        self._checker_and_import_API_modules()

    def uvicorn_runner(
        self, host: str = "localhost", port: int = settings.UVICORN_PORT
    ) -> None:
        """
        使用 uvicorn 運行 FastAPI。

        args:
            host: 伺服器的 IP (default: "localhost")
            port: 伺服器的 PORT (default: setting.UVICORN_PORT)
        """

        Logger.setup_info_log_handler()
        self._service_run()
        uvicorn.run(self, host=host, port=port)
