from enum import Enum


class StartEventTextKeywords(Enum):
    """
    Line Bot processes Event text message logic segment.
    """

    VERSION = "#秘書版本"
    QUESTION = "#文秘書"
    IMAGE_CREATOR = "#圖秘書"
