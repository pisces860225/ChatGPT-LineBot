import openai
from libs import configs


class ChatGPT_Object:
    openai.api_key = configs.OPEN_API_KEY

    @classmethod
    def chat_completion(cls, messages):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"請使用繁體中文回答，{messages}"},
            ],
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    message = "請編寫一篇文章，主題是（ChatGPT 與自媒體結合，提升品牌行銷之運用）。其中包含（Ai科技）、（市場火爆）、（多元化）"
    print(ChatGPT_Object.chat_completion(message))
