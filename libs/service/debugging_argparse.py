# -*- coding: utf-8 -*-
from libs.configs import settings
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError


class Args:
    _parser = ArgumentParser(
        description="The Bond-Agent command line tool",
        formatter_class=RawTextHelpFormatter,
    )

    @staticmethod
    def _str_to_bool(value: str) -> bool:
        """
        判斷輸入的參數是否為布林值

        args:
            value: 輸入的參數

        return:
            bool: 輸入的參數是否為布林值
        """

        if isinstance(value, bool):
            return value
        elif value.lower() in ("true", "t"):
            return True
        elif value.lower() in ("false", "f"):
            return False
        else:
            raise ArgumentTypeError(f"Invalid boolean value: {value}")

    @classmethod
    def debug_controller(cls) -> None:
        """
        設定 debug 參數
        """

        cls._parser.add_argument(
            "-d5",
            "--debug",
            default=False,
            help="debug function switch (default: False, you can use t/T/f/F/True/true/False/false to input)",
        )
        args = cls._parser.parse_args()

        settings.DEBUG = cls._str_to_bool(args.debug) if not settings.DEBUG else True
