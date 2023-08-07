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
