# -*- coding: utf-8 -*-
from libs.configs import settings
from libs.service.web_service import Service
from libs.service.debugging_argparse import Args


def main() -> None:
    """
    建立服務並啟動
    """

    Args.debug_controller()

    app = Service(
        title=settings.SERVERTITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )
    app.uvicorn_runner(host=settings.UVICORN_HOST, port=settings.UVICORN_PORT)


if __name__ == "__main__":
    main()
