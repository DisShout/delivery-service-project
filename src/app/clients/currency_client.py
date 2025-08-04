import httpx


class CurrencyClient:
    def __init__(self):
        self.url = "https://www.cbr-xml-daily.ru/daily_json.js"

    async def get_current_currency(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            data = response.json()
            rate = data["Valute"]["USD"]["Value"]
            return rate
