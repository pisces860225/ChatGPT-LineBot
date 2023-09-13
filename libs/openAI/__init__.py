import json
from libs import configs


class OpenAI_Object:
    @staticmethod
    def chat_completion(messages: str) -> str:
        """
        messages: str
        """

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

            message_content = tuple(url["url"] for url in image_urls)

        except configs.OPENAI.InvalidRequestError:
            message_content = "您輸入的關鍵字，可能不適合產生圖片，請更換關鍵字後，再試一次。"

        return message_content

    @staticmethod
    def audio_transcription(file_path: str) -> str:
        with open(file_path, "rb") as audio_file:
            response = json.loads(
                str(configs.OPENAI.Audio.transcribe("whisper-1", audio_file))
            )
        message_content = response["text"]
        return message_content

    @staticmethod
    def audio_translation(file_path: str) -> str:
        with open(file_path, "rb") as audio_file:
            response = json.loads(
                str(configs.OPENAI.Audio.translate("whisper-1", audio_file))
            )
        message_content = response["text"]
        return message_content
