from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler

import os
from libs.configs.__version__ import __version__


load_dotenv()

DEBUG = os.getenv("DEBUG")
DOCS_URL = "/PiNews_LineBot/Swagger_UI"
REDOC_URL = "/PiNews_LineBot/API_redoc"
SERVERTITLE = "PiNews_LineBot"
VERSION = __version__
HOST = "0.0.0.0"
PORT = 8000
DESCRIPTION = """
## PiNews_LineBot
# """

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

LINEBOT_API = LineBotApi(CHANNEL_ACCESS_TOKEN)
LINEBOT_HANDLER = WebhookHandler(CHANNEL_SECRET)


OPEN_API_KEY = os.getenv("OPEN_API_KEY")
