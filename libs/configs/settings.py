# -*- coding: utf-8 -*-
import sys
import openai
from pathlib import Path
from linebot import LineBotApi, WebhookHandler

from libs.configs import GetENV
from libs.configs.__version__ import __version__


# *----- Server Setting -----*
DEBUG = GetENV.get_env_variable("DEBUG")
DOCS_URL = "/LineBot/Swagger_UI"
REDOC_URL = "/LineBot/API_redoc"
SERVERTITLE = "LineBot"
VERSION = __version__
HOST = "0.0.0.0"
PORT = 8000
DESCRIPTION = """

## LineBot

"""

# *----- uvicorn Setting -----*
UVICORN_HOST = "0.0.0.0"
UVICORN_PORT = 8080

# *----- Line Bot Setting -----*
CHANNEL_ACCESS_TOKEN = GetENV.get_env_variable("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = GetENV.get_env_variable("CHANNEL_SECRET")

LINEBOT_API = LineBotApi(CHANNEL_ACCESS_TOKEN)
LINEBOT_HANDLER = WebhookHandler(CHANNEL_SECRET)


# *----- OpenAI (ChatGPT) Setting -----*
OPENAI = openai
OPENAI.api_key = GetENV.get_env_variable("OPENAI_API_KEY")
OPENAI_USE_MODEL = "gpt-3.5-turbo"


# *----- API Setting -----*
BASE_API_PATH = Path("./libs/app/API")
BASE_API_IMPORT_PATH = "libs.app.API"

# Internal API 的授權
API_ALLOW_LIST = ["line_bot.linebot_router"]

# DeBUG 的一些 API 都可以用這邊，僅 debug mode 時授權
DEBUG_API_ALLOW_LIST = []

# *----- All Logger Setting -----*
LOG_COLOR = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}

# *----- Server Access Log Setting -----*
ACCESS_LOG_NAME = "uvicorn.access"
ACCESS_LOG_SIZE = 1000  # 單位為 KB
ACCESS_LOG_LEVEL = "INFO"
ACCESS_LOG_PATH = "logs"
ACCESS_LOG_FILE_NAME = "LineBot_Backend_ACCESS_LOG.log"
ACCESS_LOG_BACKUP_COUNT = 5
ACCESS_LOG_MODE = "a"
ACCESS_LOG_ENCODING = "utf-8"

# *----- Server INFO Log Setting -----*
INFO_LOG_NAME = "LineBot Backend"
INFO_LOG_SIZE = 1000  # 單位為 KB
INFO_LOG_LEVEL = "INFO"
INFO_LOG_PATH = "logs"
INFO_LOG_FILE_NAME = "LineBot_Backend_INFO_LOG.log"
INFO_LOG_BACKUP_COUNT = 5
INFO_LOG_MODE = "a"
INFO_LOG_ENCODING = "utf-8"


# *----- System Check Setting -----*
class System:
    AIX = "aix"
    LINUX = "linux"
    WINDOWS = "win32"
    WINDOWS_CYGWIN = "cygwin"
    MAC = "darwin"


class System_Name:
    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC = "Mac"
    WINDOWS_CYGWIN = "Cygwin"
    AIX = "AIX"


SYSTEM_CHART = {
    System.AIX: "AIX",
    System.LINUX: "Linux",
    System.WINDOWS: "Windows",
    System.WINDOWS_CYGWIN: "Cygwin",
    System.MAC: "Mac",
}

OS_VERSION = sys.platform
OS_NAME = SYSTEM_CHART[OS_VERSION]
