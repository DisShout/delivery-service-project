import httpx
from src.app.core.config import settings


class CurrencyClient:
    def __init__(self):
        self.url = settings.CBR_URL

    async def get_current_currency(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            data = response.json()
            rate = data["Valute"]["USD"]["Value"]
            return rate
