import asyncio
import aiohttp
from pydantic import BaseModel, ConfigDict

class Config(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    api_url: str = "https://api.dexscreener.com/latest/dex/tokens"

class Token(BaseModel):
    name: str
    symbol: str
    price_usd: float
    volume: float

class DexScreener(BaseModel):
    config: Config

    async def fetch_trending_tokens(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.config.api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    trending_tokens = data.get("pairs", [])
                    return [
                        Token(
                            name=token.get("baseToken", {}).get("name"),
                            symbol=token.get("baseToken", {}).get("symbol"),
                            price_usd=float(token.get("priceUsd", 0)),
                            volume=float(token.get("volume", 0)),
                        )
                        for token in trending_tokens
                    ]
                else:
                    print("Failed to retrieve data from DexScreener")
                    return []

    async def run(self):
        tokens = await self.fetch_trending_tokens()
        for token in tokens:
            print(f"Name: {token.name}")
            print(f"Symbol: {token.symbol}")
            print(f"Price (USD): ${token.price_usd}")
            print(f"Volume: {token.volume}")
            print("-" * 30)