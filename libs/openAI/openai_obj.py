# -*- coding: utf-8 -*-
import json
from libs.configs import settings


class OpenAI_Object:
    @staticmethod
    def chat_completion(messages: str) -> str:
        """
        通過 OpenAI API 進行問答

        args:
            messages: str

        return:
            OpenAI 回答後的文字
        """

        response = settings.OPENAI.ChatCompletion.create(
            model=settings.OPENAI_USE_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"請使用繁體中文回答，{messages}"},
            ],
        )

        return response.choices[0].message.content.strip()
