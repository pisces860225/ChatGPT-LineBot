# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv


class GetENV:
    _loaded = False  # 類變量，用來標記 .env 文件是否已經加載過

    @staticmethod
    def load_env():
        if not GetENV._loaded:
            ENV_FILE_PATH = os.path.join(os.getcwd().replace("\\", "/"), ".env")
            load_dotenv(ENV_FILE_PATH)
            GetENV._loaded = True

    @staticmethod
    def get_env_variable(env_key: str):
        GetENV.load_env()  # 確保 .env 文件已經加載
        value = os.environ.get(env_key, None)
        if value is not None:
            if value.lower() == "true":
                return True
            elif value.lower() == "false":
                return False
        return value
