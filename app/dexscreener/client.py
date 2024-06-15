from httpx import request
import requests
import aiohttp
from pydantic import Field
from .models import TokenPair
from ..common.easymodel import EasyModel
from ..common.httpclient import HttpClient, HttpRequestMethod
from typing import Optional


class DexscreenerClientConfig(EasyModel):
    base_url: str = Field(default="https://api.dexscreener.io/latest", alias="base_url")


class DexscreenerClient(EasyModel):
    client: HttpClient = Field(default_factory=HttpClient, alias="client")
    config: DexscreenerClientConfig = Field(default_factory=DexscreenerClientConfig, alias="config")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client.config.base_url = self.config.base_url
        pass
    
    def get_token_pair(self, chain: str, address: str) -> Optional[TokenPair]:
        """
        Fetch a pair on the provided Blockchain with the provided Contract Address.
        """
        response = self.client.api_request(HttpRequestMethod.GET, f"dex/pairs/{chain}/{address}")
        return TokenPair(**response["pair"]) if response["pair"] else None

    async def get_token_pair_async(self, chain: str, address: str) -> Optional[TokenPair]:
        """
        Async version of `get_token_pair` method - Fetch a pair on the provided Blockchain with the provided Contract Address.
        """
        response = await self.client.api_request_async(HttpRequestMethod.GET, f"dex/pairs/{chain}/{address}")
        return TokenPair(**response["pair"]) if response["pair"] else None

    def get_token_pairs(self, address: str) -> list[TokenPair]:
        """
        Get pairs matching the provided Contract Address.
        """
        response = self.client.api_request(HttpRequestMethod.GET,  f"dex/tokens/{address}")
        return [TokenPair(**pair) for pair in response] if len(response) > 0 else []

    async def get_token_pairs_async(self, address: str) -> list[TokenPair]:
        """
        Async version of `get_token_pairs`.
        """
        response = await self.client.api_request_async(HttpRequestMethod.GET, f"dex/tokens/{address}")
        return [TokenPair(**pair) for pair in response] if len(response) > 0 else []

    def search_pairs(self, search_query: str) -> list[TokenPair]:
        """
        Search for pairs matching query
        """
        response = self.client.api_request("dex/search", HttpRequestMethod.GET, params={"q": search_query})
        return [TokenPair(**pair) for pair in response.get("pairs", [])] if len(response.get("pairs", [])) > 0 else []

    async def search_pairs_async(self, search_query: str) -> list[TokenPair]:
        """
        Async version of `search_pairs`
        """
        response = await self.client.api_request_async("dex/search", HttpRequestMethod.GET, params={"q": search_query})
        return [TokenPair(**pair) for pair in response.get("pairs", [])] if len(response.get("pairs", [])) > 0 else []

