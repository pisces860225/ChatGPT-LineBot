# -*- coding: utf-8 -*-
import os
import sys
import logging

from libs.configs import settings


class AccessLogger:
    @classmethod
    def _setup_log_directory(cls) -> None:
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
    def setup_access_log_handler(cls) -> None:
        """
        建立 access log handler，並定義 log 的等級及格式
        """

        cls._setup_log_directory()

        # 取得 access log handler 物件，並設定 log 等級
        cls.access_logger = logging.getLogger(settings.ACCESS_LOG_NAME)
        cls.access_logger.setLevel(
            logging.DEBUG if settings.DEBUG else settings.ACCESS_LOG_LEVEL
        )

        # 建立 access log file 所使用的 handler
        handler = logging.handlers.RotatingFileHandler(
            filename=rf"{cls.localpath}/{settings.ACCESS_LOG_PATH}/{settings.ACCESS_LOG_FILE_NAME}",
            mode=settings.ACCESS_LOG_MODE,
            encoding=settings.ACCESS_LOG_ENCODING,
            maxBytes=settings.ACCESS_LOG_SIZE * 1024,
            backupCount=settings.ACCESS_LOG_BACKUP_COUNT,
        )

        # 建立自訂的 log 格式
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(name)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
            )
        )

        # 將 handler 註冊進 logger
        cls.access_logger.addHandler(handler)
