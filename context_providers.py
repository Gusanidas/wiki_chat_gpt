import json
import asyncio
import tiktoken
import wiki_api
import openai_api
from mytypes import ConversationLog, Message
from typing import List, Union

class ContextProvider():

    async def get_context(self, conversation_log: ConversationLog, *args, **kwargs) -> ConversationLog:
        return conversation_log

class WikiContextProvider(ContextProvider):

    def __init__(self):
        self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.max_tokens = 3200
        self.get_wiki_terms_prompt = None
        with open("get_wiki_terms_prompt.json", "r") as f:
            self.get_wiki_terms_prompt = json.load(f)

    async def add_context(self, conversation_log: ConversationLog, temperature: float = 0.9) -> ConversationLog:
        suggestions = await self._get_possible_wiki_pages(conversation_log[-1], temperature)
        new_conversation_log = conversation_log
        if suggestions:
            pages = await asyncio.gather(*[self._get_title(suggestion) for suggestion in suggestions])
            pages = [page for page in pages if page is not None]
            #print(f"pages: {pages}")
            summaries = await self._get_summary("|".join(pages))
            context_message, total_tokens = self._build_context_message(summaries, conversation_log[-1]["content"])
            new_conversation_log = self._get_new_conversation_log(conversation_log, context_message, total_tokens)
        return new_conversation_log

    async def _get_possible_wiki_pages(self, message: Message, temperature: float) -> List[str]:
        if self.get_wiki_terms_prompt is None:
            return []
        else:
            message_log = self.get_wiki_terms_prompt + [message]
            r = await openai_api.get_chat_completion(message_log, temperature)
            return self._parse_wiki_pages(r["choices"][0]["message"]["content"])

    def _parse_wiki_pages(self, response: str) -> List[str]:
        return [line.strip().lstrip("- ") for line in response.split("\n") if line.startswith("- ")]
        
    async def _get_title(self, suggestion: str) -> Union[str, None]:
       title_result = await wiki_api.search_title(suggestion)
       return title_result["query"]["search"][0]["title"] if title_result["query"]["search"] else None

    async def _get_summary(self, titles: str) -> List[str]:
        summary_results = await wiki_api.get_summary(titles)
        summary_extracts = [page["extract"] for page in summary_results["query"]["pages"].values() if "extract" in page]
        return summary_extracts

    def _build_context_message(self, summaries: List[str], last_message: str) -> tuple[str, int]:
        context_message, total_tokens = "", len(self.tokenizer.encode(last_message))
        for page in summaries:
            token_length = len(self.tokenizer.encode(page))
            if total_tokens + token_length < self.max_tokens:
                context_message += page
                total_tokens += token_length
            else:
                break
        return context_message, total_tokens
    
    def _get_new_conversation_log(self, conversation_log: ConversationLog, context_message: str, total_tokens: int):
        new_conversation_log = []
        for message in conversation_log[:0:-1]:
            token_length = len(self.tokenizer.encode(message["content"]))
            if total_tokens + token_length < self.max_tokens:
                total_tokens += token_length
                new_conversation_log.append(message)
            else:
                break
        new_conversation_log.reverse()
        new_conversation_log.append({"role": "user", "content": context_message})
        new_conversation_log.append({"role": "system", "content": "Ok"})
        new_conversation_log.append(conversation_log[-1])
        return new_conversation_log
        

        

            
