import os
import aiohttp
from dotenv import load_dotenv 
from mytypes import ConversationLog

load_dotenv()

async def get_chat_completion(messages: ConversationLog, temperature: float = 1):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": temperature
        }
        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data) as response:
            response_json = await response.json()
            return response_json

