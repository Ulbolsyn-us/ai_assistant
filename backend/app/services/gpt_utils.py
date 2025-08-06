import os
import httpx
from dotenv import load_dotenv

load_dotenv()
    
async def ask_gpt(message: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI-Assistant Demo"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are helpful assistant."},
            {"role": "user", "content": message}
        ] 
    }
    async with httpx.AsyncClient(timeout=30.0) as client: 
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    return response.choices[0].message.content
