import aiohttp
import asyncio

API_URL = 'http://en.wikipedia.org/w/api.php'

async def get_summary(title):
    summary_params = {
        'prop': 'extracts',
        'explaintext': '',
        'exintro': '',
        'titles': title,
        'format': 'json',
        'action': 'query'
      }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=summary_params) as response:
            data = await response.json()
            return data

async def search_title(title, limit = 1):
    search_params = {
    'list': 'search',
    'srprop': '',
    'srlimit': limit,
    'srsearch': title,
    'format': 'json',
    'action': 'query'
  }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=search_params) as response:
            data = await response.json()
            return data