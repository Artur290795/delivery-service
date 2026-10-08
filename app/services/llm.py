from openai import AsyncOpenAI

from app.config import settings


class LLMService:
    def __init__(self, api_key: str, folder_id: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.yandex_api_base_url,
        )
        self.model_uri = f"gpt://{folder_id}/{settings.yandex_model_name}"

    async def generate_answer(self, question: str, context: str):
        response = await self.client.chat.completions.create(
            model=self.model_uri,
            messages=[
                {
                    "role": "system",
                    "content": """
            Ты отвечаешь на вопросы пользователей службы доставки.
            Используй только предоставленный контекст.
            Если в контексте нет ответа — сообщи об этом.
        """,
                },
                {
                    "role": "user",
                    "content": f"""
            Контекст:
            {context}

            Вопрос:
            {question}
        """,
                },
            ],
        )
        return response.choices[0].message.content
