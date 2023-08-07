import openai
from libs import configs


class ChatGPT_Object:
    openai.api_key = configs.OPEN_API_KEY

    @classmethod
    def chat_completion(cls, messages):
        response = openai.ChatCompletion.create(
            model=configs.CHATGPT_USE_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"請使用繁體中文回答，{messages}"},
            ],
        )
        return response.choices[0].message.content.strip()
