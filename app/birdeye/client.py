from typing import List, Optional, Dict, Any, Union
from pydantic import Field, HttpUrl

from .models import DefiNetwork, HistoryResponse, NetworkResponse, PriceResponse, SupportedNetworks
from ..common.easymodel import EasyModel
from ..common.httpclient import HttpClient, HttpRequestMethod


class BirdeyeClientConfig(EasyModel):
    """
	Configuration for the BirdeyeClient class.
    """
    base_url: HttpUrl = Field(default=HttpUrl(
        "https://public-api.birdeye.so/defi"), alias="base_url")
    api_key: str = Field(..., alias="api_key")


class BirdeyeClient(EasyModel):
	"""
	A simple rate-limited HTTP client for making requests to the Birdeye API.
	"""
	client: HttpClient = Field(default_factory=HttpClient, alias="client")
	config: BirdeyeClientConfig = Field(
	    default_factory=BirdeyeClientConfig, alias="config")

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.client.config.base_url = self.config.base_url
		pass

	def get_supported_networks(self) -> list[DefiNetwork]:
		"""
		Get all supported networks by Birdeye.
		"""
		response = self.client.api_request(endpoint="networks", method=HttpRequestMethod.GET, headers={'X-API-KEY': self.config.api_key,})
		if response['success'] == True:
			return [DefiNetwork(network) for network in response["data"]] if response["data"] is not None and len(response["data"]) > 0 else []
		return []

	async def get_supported_networks_async(self) -> list[DefiNetwork]:
		"""
		Async version of `get_supported_networks` method - Get all supported networks by Birdeye.
		"""
		response = await self.client.api_request_async(endpoint="networks", method=HttpRequestMethod.GET, headers={'X-API-KEY': self.config.api_key,},)
		if response['success'] == True:
			return [DefiNetwork(network) for network in response["data"]] if response["data"] is not None and len(response["data"]) > 0 else []
		return []

	def get_price(self, address: str) -> PriceResponse:
		response = self.client.api_request(
            f"price",
            HttpRequestMethod.GET,
            params={
				'address': address,
			},
            headers={
				'X-API-KEY': self.config.api_key,
			}
        )
		return PriceResponse(**response)

	async def get_price_async(self, address: str) -> PriceResponse:
		response = await self.client.api_request_async(
            f"price?address={address}",
            HttpRequestMethod.GET,
            params={
				'address': address,
			},
            headers={
				'X-API-KEY': self.config.api_key,
			}
        )
		return PriceResponse(**response)

	def get_multi_price(self, addresses: List[str]) -> PriceResponse:
		address_list = ",".join(addresses)
		response = self.client.api_request(
            f"multi_price",
            HttpRequestMethod.GET,
            params={
				'list_address': address_list,
			},
            headers={
				'X-API-KEY': self.config.api_key,
			}
        )
		return PriceResponse(**response)

	async def get_multi_price_async(self, addresses: List[str]) -> PriceResponse:
		response = await self.client.api_request_async(
            f"multi_price",
            HttpRequestMethod.GET,
            params={
				'list_address': ",".join(addresses),
			},
            headers={
				'X-API-KEY': self.config.api_key,
			}
        )
		return PriceResponse(**response)
