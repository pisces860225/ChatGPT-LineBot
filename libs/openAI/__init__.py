import json
from libs import configs


class ChatBot_Object:
    @staticmethod
    def chat_completion(messages: str) -> str:
        response = configs.OPENAI.ChatCompletion.create(
            model=configs.OPENAI_USE_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"請使用繁體中文回答，{messages}"},
            ],
        )
        return response.choices[0].message.content.strip()

    @staticmethod
    def image_completion(prompt: str, size: str = "1024x1024") -> str | tuple[str]:
        try:
            response = json.loads(
                str(configs.OPENAI.Image.create(prompt=prompt, n=2, size=size))
            )

            image_urls = response["data"]

            message_content = (url["url"] for url in image_urls)

        except configs.OPENAI.InvalidRequestError:
            message_content = "您輸入的關鍵字，可能不適合產生圖片，請更換關鍵字後，再試一次。"

        return message_content
