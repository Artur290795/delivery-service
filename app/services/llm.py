from openai import AsyncOpenAI


class LLMService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_answer(self, question: str, context: str):
        response = await self.client.responses.create(
            model="gpt-5.6-luna",
            input=f"""
                    Ответь на вопрос пользователя, используя только информацию из контекста.
                    Контекст:
                    {context}

                    Вопрос:
                    {question}
                    """,
        )
        return response.output_text
