from enum import Enum


class StartEventTextKeywords(Enum):
    """
    Line Bot processes Event text message logic segment.
    """

    VERSION = "#先知版本"
    QUESTION = "#秘書"
    CANDO_LIST = "#能做什麼"
