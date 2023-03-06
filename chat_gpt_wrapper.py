import asyncio
import tiktoken
import openai_api
from  context_providers import ContextProvider
from typing import Union
from mytypes import Message


class ChatGptWrapper:

    def __init__(self, context_provider: Union[ContextProvider, None] = None):
        self.context_provider = context_provider
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.total_max_tokens = 4096
        self.conversation_log = [{"role": "system", "content": "You are a helpful assistant."}]
        self.current_tokens = len(self.tokenizer.encode(self.conversation_log[0]["content"]))

    async def get_response(self, user_prompt: str) -> str:
        self._add_to_conversation_log({"role": "user", "content": user_prompt})
        self._trim_conversation_log()
        if self.context_provider:
            conversation_log_with_context = await self.context_provider.add_context(self.conversation_log)
            response = await openai_api.get_chat_completion(conversation_log_with_context)
        else:
            response = await openai_api._get_chat_completion(self.conversation_log)
        self._add_to_conversation_log(response["choices"][0]["message"])
        return response["choices"][0]["message"]["content"]
    
    def sync_get_response(self, user_prompt: str) -> str:
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_response(user_prompt))
        return response
    
    def _add_to_conversation_log(self, message: Message):
        self.conversation_log.append(message)
        self.current_tokens += len(self.tokenizer.encode(message["content"]))

    def _trim_conversation_log(self):
        while self.current_tokens > self.total_max_tokens:
            last_message = self.conversation_log.pop(0)
            self.current_tokens -= len(self.tokenizer.encode(last_message["content"]))


