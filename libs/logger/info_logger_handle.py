# -*- coding: utf-8 -*-
import os
import sys
import logging

from libs.configs import settings
from libs.logger.logger_format import ColoredFormatter


class Logger:
    @classmethod
    def _setup_log_directory(cls):
        """
        初始化時檢查 logs 目錄是否存在，如果不存在則建立

        args:
            log_path: log 的存放路徑
        """

        cls.localpath = (
            os.getcwd().replace("\\", "/")
            if sys.platform == settings.System.WINDOWS
            else os.getcwd()
        )

        cls.logs_path = os.path.join(cls.localpath, settings.ACCESS_LOG_PATH)

        if not os.path.isdir(cls.logs_path):
            os.makedirs(cls.logs_path)

    @classmethod
    def setup_info_log_handler(cls) -> None:
        """
        建立 info log handler，並定義 log 的等級及格式
        """

        cls._setup_log_directory()

        # 取得 info log handler 物件，並設定 log 等級
        cls.info_logger = logging.getLogger(settings.INFO_LOG_NAME)
        cls.info_logger.setLevel(
            logging.DEBUG if settings.DEBUG else settings.INFO_LOG_LEVEL
        )

        # 建立 info log file 所使用的 handler
        file_handler = logging.handlers.RotatingFileHandler(
            filename=rf"{cls.localpath}/{settings.INFO_LOG_PATH}/{settings.INFO_LOG_FILE_NAME}",
            mode=settings.INFO_LOG_MODE,
            encoding=settings.INFO_LOG_ENCODING,
            maxBytes=settings.INFO_LOG_SIZE * 1024,
            backupCount=settings.INFO_LOG_BACKUP_COUNT,
        )

        # 建立 console log 所使用的 handler
        console_handler = logging.StreamHandler()

        # 建立自訂的 log 格式
        colored_formatter = ColoredFormatter(
            "%(asctime)s %(name)s [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S",
            use_colors=True,
        )
        plain_formatter = ColoredFormatter(
            "%(asctime)s %(name)s [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S",
            use_colors=False,
        )

        # 分別套用 log 的格式給不同的 handler
        console_handler.setFormatter(colored_formatter)
        file_handler.setFormatter(plain_formatter)

        # 將 handler 註冊進 logger
        cls.info_logger.addHandler(console_handler)
        cls.info_logger.addHandler(file_handler)

    @classmethod
    def _log(cls, level: str, msg: str, msg_color: str = None, *args, **kwargs) -> None:
        """
        重新包裝 logging 方法，並且可以自訂 log message 的顏色

        args:
            level: log 的等級
            msg: log 的訊息
            msg_color: log 訊息的顏色
            *args: logging 方法所需要的參數
            **kwargs: logging 方法所需要的參數
        """

        # 如果 msg_color 有值，則將顏色加入 log message
        if msg_color:
            extra = {"message_color": msg_color}
            if "extra" in kwargs:
                kwargs["extra"].update(extra)
            else:
                kwargs["extra"] = extra

        # 透過 getattr 取得 logger 物件的方法，並執行
        getattr(cls.info_logger, level)(msg, *args, **kwargs)

    @classmethod
    def supported_colors(cls) -> None:
        """
        呈現 log 目前支援的顏色
        """

        for color in list(settings.LOG_COLOR.keys()):
            cls._log("info", f"Supported Color: {color}", color)

    @classmethod
    def debug(cls, msg: str, color="green", *args, **kwargs) -> None:
        """
        重新包裝 logging.debug 方法，並且可以自訂 log message 的顏色

        args:
            msg: log 的訊息
            color: log 訊息的顏色 (default: green)
            *args: logging 方法所需要的參數
            **kwargs: logging 方法所需要的參數
        """

        cls._log("debug", msg, color, *args, **kwargs)

    @classmethod
    def info(cls, msg: str, color="white", *args, **kwargs) -> None:
        """
        重新包裝 logging.info 方法，並且可以自訂 log message 的顏色

        args:
            msg: log 的訊息
            color: log 訊息的顏色 (default: white)
            *args: logging 方法所需要的參數
            **kwargs: logging 方法所需要的參數
        """

        cls._log("info", msg, color, *args, **kwargs)

    @classmethod
    def warning(cls, msg: str, color="yellow", *args, **kwargs) -> None:
        """
        重新包裝 logging.warning 方法，並且可以自訂 log message 的顏色

        args:
            msg: log 的訊息
            color: log 訊息的顏色 (default: yellow)
            *args: logging 方法所需要的參數
            **kwargs: logging 方法所需要的參數
        """

        cls._log("warning", msg, color, *args, **kwargs)

    @classmethod
    def error(cls, msg: str, color="red", *args, **kwargs) -> None:
        """
        重新包裝 logging.critical 方法，並且可以自訂 log message 的顏色

        args:
            msg: log 的訊息
            color: log 訊息的顏色 (default: white)
            *args: logging 方法所需要的參數
            **kwargs: logging 方法所需要的參數
        """

        cls._log("error", msg, color, *args, **kwargs)

    @classmethod
    def critical(cls, msg: str, color="white", *args, **kwargs) -> None:
        """
        重新包裝 logging.critical 方法，並且可以自訂 log message 的顏色
        """

        cls._log("critical", msg, color, *args, **kwargs)
