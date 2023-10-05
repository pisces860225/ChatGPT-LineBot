# -*- coding: utf-8 -*-
import logging
from typing import Iterable
from termcolor import colored

from libs.configs import settings


class ColoredFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        style: str = "%",
        use_colors: bool = True,
    ) -> None:
        super().__init__(fmt, datefmt, style)
        self.use_colors = use_colors

    def colored_text(self, text: str, color: str, attrs: Iterable[str] = ()) -> str:
        """
        將文字加上顏色，並回傳帶有顏色的文字

        args:
            text: 要加上顏色的文字
            color: 要加上的顏色
            attrs: 要加上的屬性

        return:
            帶有顏色的文字
        """

        return colored(text, color, attrs=attrs) if self.use_colors else text

    def format(self, record: logging.LogRecord) -> str:
        """
        建立一個自訂的 log 格式，並且可以自訂 log 等級的顏色

        args:
            record: log 的紀錄

        return:
            拼裝後的 log 訊息
        """

        super().format(record)
        color = settings.LOG_COLOR.get(record.levelname)

        time_color = "blue"
        name_color = "magenta"
        message_color = getattr(record, "message_color", "white")
        dividing_line_color = "white"

        # 建立 log 等級的文字並加上顏色
        log_level = "{} {} {} {} {}".format(
            self.colored_text("|", dividing_line_color, attrs=["bold"]),
            self.colored_text(record.name.upper(), name_color, attrs=["bold"]),
            self.colored_text("|", dividing_line_color, attrs=["bold"]),
            self.colored_text(record.levelname.upper(), color, attrs=["bold"]),
            self.colored_text("|", dividing_line_color, attrs=["bold"]),
        )

        # 回傳拼裝後的 log 訊息
        return "{} {} {}".format(
            self.colored_text(record.asctime, time_color, attrs=["bold"]),
            log_level,
            self.colored_text(record.getMessage(), message_color, attrs=["bold"]),
        )
