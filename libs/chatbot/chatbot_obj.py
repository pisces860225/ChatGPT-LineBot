# -*- coding: utf-8 -*-
from typing import List
from linebot.models import TextSendMessage, ImageSendMessage

from libs.configs import settings


class LineBot_Object:
    @staticmethod
    def reply_text_to_user(event, response_text: str) -> None:
        """
        Sends a reply to the user.
        """
        settings.LINEBOT_API.reply_message(
            event.reply_token, TextSendMessage(text=response_text)
        )

    @staticmethod
    def reply_image_to_user(event, url: str) -> None:
        """
        Sends a reply to the user.
        """
        settings.LINEBOT_API.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url,
            ),
        )

    @staticmethod
    def reply_text_and_image_to_user(event, response_text: str, url: str) -> None:
        """
        Sends a reply to the user.
        """
        settings.LINEBOT_API.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=response_text),
                ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url,
                ),
            ],
        )

    @staticmethod
    def reply_images_to_user(event, urls: List[str]) -> None:
        """
        Sends a reply to the user.
        """

        settings.LINEBOT_API.reply_message(
            event.reply_token,
            [
                ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url,
                )
                for url in urls
            ],
        )

    @staticmethod
    def reply_text_and_images_to_user(
        event, response_text: str, urls: List[str]
    ) -> None:
        """
        Sends a reply to the user.
        """
        text_message = [TextSendMessage(text=response_text)]
        image_message = [
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url,
            )
            for url in urls
        ]
        settings.LINEBOT_API.reply_message(
            event.reply_token,
            text_message + image_message,
        )
