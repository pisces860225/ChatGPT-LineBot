import os
import logging
from libs import configs


class Logger:
    @staticmethod
    def setup_logger(log_name: str) -> None:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.getLevelName(configs.ACCESS_LOG_LEVEL))
        localpath = os.getcwd().replace("\\", "/")
        logs_path = localpath + "/" + configs.ACCESS_LOG_PATH

        if not os.path.isdir(logs_path):
            os.makedirs(logs_path)

        handler = logging.handlers.RotatingFileHandler(
            filename=rf"{localpath}/{configs.ACCESS_LOG_PATH}/{configs.ACCESS_LOG_FILE_NAME}",
            mode=configs.ACCESS_LOG_MODE,
            encoding=configs.ACCESS_LOG_ENCODING,
            maxBytes=configs.ACCESS_LOG_SIZE * 1024,
            backupCount=configs.ACCESS_LOG_BACKUP_COUNT,
        )

        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s [%(levelname)s] | %(message)s")
        )

        logger.addHandler(handler)
