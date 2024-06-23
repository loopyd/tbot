from functools import wraps
from pydantic import Field

from ..birdeye.models import DefiNetwork
from .models import TokenPair
from ..common.easymodel import EasyModel
from ..common.httpclient import HttpClient, HttpRequestMethod
from typing import Any, Callable, Dict, List, Union


class DexscreenerClientConfig(EasyModel):
    base_url: str = Field(
        default="https://api.dexscreener.io/latest", alias="base_url")


def dexscreener_route() -> Callable[..., Callable[..., Any]]:
    """
    Dexscreener API route.

    This decorator is used to wrap methods that make requests to the Dexscreener API.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            key: Union[str, List[str]] = kwargs.get('address', "")
            if key:
                if isinstance(key, list) and len(key) > 0:
                    kwargs['address'] = key
                elif isinstance(key, str) and len(key) > 0:
                    kwargs['address'] = key
                else:
                    raise ValueError(f"Invalid address provided: {key}")
            response = func(self, *args, **kwargs)
            result: List[TokenPair] | None = [TokenPair(**pair) for pair in response.get("pairs", [])] if response.get("pairs", []) is not None else None
            if result is not None:
                if len(result) == 1:
                    return result[0]
                return result
            else:
                return None
        return wrapper
    return decorator


def dexscreener_route_async() -> Callable[..., Callable[..., Any]]:
    """
    Asyncronous Dexscreener API route.

    This decorator is used to wrap async methods that make requests to the Dexscreener API.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=func)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            key = kwargs.get('address', "")
            if isinstance(key, list) or isinstance(key, str):
                if isinstance(key, list) and len(key) > 0:
                    kwargs['address'] = key
                elif isinstance(key, str) and len(key) > 0:
                    kwargs['address'] = key
                else:
                    raise ValueError(f"Invalid address provided: {key}")
            response = await func(self, *args, **kwargs)
            result: List[TokenPair] | None = [TokenPair(**pair) for pair in response.get("pairs", [])
                      ] if response.get("pairs", []) is not None else None
            if result is not None:
                if len(result) == 1:
                    return result[0]
                return result
            else:
                return None
        return wrapper
    return decorator


class DexscreenerClient(EasyModel):
    """
    A simple rate-limited HTTP client for making requests to the Dexscreener API.
    """
    client: HttpClient = Field(default_factory=HttpClient, alias="client")
    config: DexscreenerClientConfig = Field(
        default_factory=DexscreenerClientConfig, alias="config")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.client.config.base_url = self.config.base_url

    @dexscreener_route()
    def get_pairs(self, address: Union[str, List[str]], network: DefiNetwork) -> Union[TokenPair, List[TokenPair], Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Fetch pairs on the provided Blockchain with the provided Contract Address.
        """
        return self.client.api_request(f"dex/pairs/{network.value}/{address}", HttpRequestMethod.GET)

    @dexscreener_route_async()
    async def get_pairs_async(self, address: Union[str, List[str]], network: DefiNetwork) -> Union[TokenPair, List[TokenPair], Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Async version of `get_token_pair` method - Fetch pairs on the provided Blockchain with the provided Contract Address.
        """
        return await self.client.api_request_async(f"dex/pairs/{network.value}/{address}", HttpRequestMethod.GET)

    @dexscreener_route()
    def get_tokens(self, address: Union[str, List[str]]) -> Union[TokenPair, List[TokenPair], Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Get pairs matching the provided Contract Address.
        """
        return self.client.api_request(f"dex/tokens/{address}", HttpRequestMethod.GET)

    @dexscreener_route_async()
    async def get_tokens_async(self, address: str) -> Union[TokenPair, List[TokenPair], Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Async version of `get_token_pairs`.
        """
        return await self.client.api_request_async(f"dex/tokens/{address}", HttpRequestMethod.GET)

    @dexscreener_route()
    def search_pairs(self, search_query: str) -> Union[TokenPair, List[TokenPair], Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Search for pairs matching query
        """
        return self.client.api_request("dex/search", HttpRequestMethod.GET, params={"q": search_query})

    @dexscreener_route_async()
    async def search_pairs_async(self, search_query: str) -> Union[TokenPair, List[TokenPair], Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Async version of `search_pairs`
        """
        return await self.client.api_request_async("dex/search", HttpRequestMethod.GET, params={"q": search_query})
