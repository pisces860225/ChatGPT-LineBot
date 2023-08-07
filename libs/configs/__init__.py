import os
import openai
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler

from libs.configs.__version__ import __version__

# read .env file
load_dotenv()

# *----- piNews Server Setting -----*
DEBUG = os.getenv("DEBUG")
DOCS_URL = "/PiNews_LineBot/Swagger_UI"
REDOC_URL = "/PiNews_LineBot/API_redoc"
SERVERTITLE = "PiNews_LineBot"
VERSION = __version__
HOST = "0.0.0.0"
PORT = 8000
DESCRIPTION = """

## PiNews_LineBot

"""

# *----- Line Bot Setting -----*
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
LINEBOT_API = LineBotApi(CHANNEL_ACCESS_TOKEN)
LINEBOT_HANDLER = WebhookHandler(CHANNEL_SECRET)

STARTEVENT_TEXT = "#秘書"  # 設定觸發事件的文字


# *----- OpenAI (ChatGPT) Setting -----*
OPENAI = openai
OPENAI.api_key = os.getenv("OPEN_API_KEY")
OPENAI_USE_MODEL = "gpt-3.5-turbo"


# *----- Server Access Log Setting -----*
ACCESS_LOG_NAMES = ["uvicorn", "uvicorn.access", "uvicorn.error"]
ACCESS_LOG_SIZE = 1000  # 單位為 KB
ACCESS_LOG_LEVEL = "DEBUG"
ACCESS_LOG_PATH = "logs"
ACCESS_LOG_FILE_NAME = "piNews_LineBot_ACCESS_LOG.log"
ACCESS_LOG_BACKUP_COUNT = 5
ACCESS_LOG_MODE = "a"
ACCESS_LOG_ENCODING = "utf-8"
