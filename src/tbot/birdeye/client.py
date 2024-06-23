from typing import Any, List, Optional
from pydantic import Field, HttpUrl

from .models import DefiNetwork, TokenPrice
from ..common.easymodel import EasyModel
from ..common.httpclient import HttpClient, HttpRequestMethod


class BirdeyeClientConfig(EasyModel):
    """
    Configuration for the BirdeyeClient class.
    """
    base_url: Optional[HttpUrl] = Field(default="https://public-api.birdeye.so/defi", alias="base_url")
    api_key: Optional[str] = Field(default=None, alias="api_key")


class BirdeyeClient(EasyModel):
    """
    A simple rate-limited HTTP client for making requests to the Birdeye API.
    """
    client: HttpClient = Field(default_factory=HttpClient, alias="client")
    config: BirdeyeClientConfig = Field(
        default_factory=BirdeyeClientConfig, alias="config")

    def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.client.config.base_url = self.config.base_url
        self.config.api_key = kwargs.get("api_key", None)

    def get_supported_networks(self) -> list[DefiNetwork]:
        """
        Get all supported networks by Birdeye.
        """
        response = self.client.api_request(
            endpoint="networks",
            method=HttpRequestMethod.GET,
            headers={
                "X-API-KEY": self.config.api_key,
            },
        )
        if response["success"] == True:
            return (
                [DefiNetwork(value=network) for network in response["data"]]
                if response["data"] is not None and len(response["data"]) > 0
                else []
            )
        return []

    async def get_supported_networks_async(self) -> list[DefiNetwork]:
        """
        Async version of `get_supported_networks` method - Get all supported networks by Birdeye.
        """
        response = await self.client.api_request_async(
            endpoint="networks",
            method=HttpRequestMethod.GET,
            headers={
                "X-API-KEY": self.config.api_key,
            },
        )
        if response["success"] == True:
            return (
                [DefiNetwork(value=network) for network in response["data"]]
                if response["data"] is not None and len(response["data"]) > 0
                else []
            )
        return []

    def get_price(
        self,
        address: str,
        network: Optional[DefiNetwork] = DefiNetwork.SOLANA,
        check_liquidity: Optional[int] = None,
        include_liquidity: Optional[bool] = None,
    ) -> TokenPrice:
        """
		Get the price of a token.
        """
        response = self.client.api_request(
            "price",
            HttpRequestMethod.GET,
            params={
                "address": address,
                **({"check_liquidity": "true" if check_liquidity else "false"} if check_liquidity is not None else {}),
                **({"include_liquidity": include_liquidity} if include_liquidity is not None else {}),
            },
            headers={"X-API-KEY": self.config.api_key,
                     "X-CHAIN": network.value},
        )
        return TokenPrice(**response.get("data", {}))

    async def get_price_async(
        self,
        address: str,
        network: Optional[DefiNetwork] = DefiNetwork.SOLANA,
        check_liquidity: Optional[int] = None,
        include_liquidity: Optional[bool] = None,
    ) -> TokenPrice:
        """
		Async version of `get_price` method - Get the price of a token.
        """
        response = await self.client.api_request_async(
            "price",
            HttpRequestMethod.GET,
            params={
                "address": address,
                **({"check_liquidity": "true" if check_liquidity else "false"} if check_liquidity is not None else {}),
                **({"include_liquidity": include_liquidity} if include_liquidity is not None else {}),
            },
            headers={"X-API-KEY": self.config.api_key,
                     "X-CHAIN": network.value},
        )
        return TokenPrice(**response.get("data", {}))

    def get_multi_price(self, addresses: List[str]) -> List[TokenPrice]:
        """
		Get the price of multiple tokens.
        """
        address_list: str = ",".join(addresses)
        response = self.client.api_request(
            "multi_price",
            HttpRequestMethod.GET,
            params={
                "list_address": address_list,
            },
            headers={
                "X-API-KEY": self.config.api_key,
            },
        )
        return [TokenPrice(**token) for token in response.get("data", [])]

    async def get_multi_price_async(self, addresses: List[str]) -> List[TokenPrice]:
        """
		Async version of `get_multi_price` method - Get the price of multiple tokens.
        """
        response = await self.client.api_request_async(
            f"multi_price",
            HttpRequestMethod.GET,
            params={
                "list_address": ",".join(addresses),
            },
            headers={
                "X-API-KEY": self.config.api_key,
            },
        )
        return [TokenPrice(**token) for token in response.get("data", [])]
