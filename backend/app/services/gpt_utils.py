import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def ask_gpt(message: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        # Логируем ошибку и возвращаем внятный ответ
        print("❌ OPENROUTER_API_KEY не найден в переменных окружения")
        return "Ошибка: API-ключ OpenRouter не настроен."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://ai-assistant-a7mq.onrender.com",
        "X-Title": "AI-Assistant Demo",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=data)
            if response.status_code != 200:
                print(f"❌ Ошибка OpenRouter: {response.status_code} {response.text}")
                return f"Ошибка запроса: {response.status_code}"

            resp_json = response.json()
            return resp_json["choices"][0]["message"]["content"]

    except httpx.HTTPError as e:
        print(f"❌ Ошибка HTTP-запроса: {e}")
        return "Ошибка при соединении с моделью."