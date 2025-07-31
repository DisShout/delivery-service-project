import redis.asyncio as aioredis
from src.app.clients.currency_client import CurrencyClient
from src.app.core.config import get_settings

settings = get_settings()


class CurrencyService:
    def __init__(self):
        self.redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            decode_responses=True,
        )
        self.cache_key = "usd_to_rub"
        self.currency_client = CurrencyClient()

    async def get_usd_to_rub(self) -> float:
        rate = await self.redis.get(self.cache_key)

        if rate:
            return float(rate)

        rate = await self.currency_client.get_current_currency()

        await self.redis.set(self.cache_key, rate, ex=60 * 30)  # ttl 30 minutes

        return float(rate)
