from enum import Enum
from pydantic import Field, HttpUrl, computed_field
import requests
from typing import Any, Dict, List, Optional, Tuple, Type, Union
import aiohttp

from .retry import retry_on_error, retry_on_error_async
from .ratelimit import RateLimiter, rate_limit, rate_limit_async
from .easymodel import EasyModel


class HttpRequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpClientConfig(EasyModel):
    """
    Configuration for the Rate-Limited HttpClient class.
    """
    base_url: HttpUrl = Field(
        default=HttpUrl("https://api.dexscreener.io/latest"), alias="base_url")
    ratelimit_max_calls: int = Field(default=300, alias="ratelimit_max_calls")
    ratelimit_period: int = Field(default=60, alias="ratelimit_period")


class HttpRequest(EasyModel):
    url: Optional[HttpUrl] = Field(None, alias="url")
    method: Optional[HttpRequestMethod] = Field(
        default=HttpRequestMethod.GET, alias="method")
    params: Optional[Union[Dict[str, Any], List[Tuple[str, Any]], bytes]] = Field(
        None, alias="params")
    data: Optional[Union[Dict[str, Any], List[Tuple[str, Any]],
                         bytes, Any]] = Field(None, alias="data")
    body: Optional[Any] = Field(None, alias="body")
    headers: Optional[Dict[str, str]] = Field(None, alias="headers")
    cookies: Optional[Union[Dict[str, str], Any]
                      ] = Field(None, alias="cookies")
    files: Optional[Dict[str, Union[Any, Tuple[str, Any, Optional[str],
                                               Optional[Dict[str, str]]]]]] = Field(None, alias="files")
    auth: Optional[Union[Tuple[str, str], Any]] = Field(None, alias="auth")
    timeout: Optional[Union[float, Tuple[float, float]]
                      ] = Field(None, alias="timeout")
    allow_redirects: Optional[bool] = Field(None, alias="allow_redirects")
    proxies: Optional[Dict[str, str]] = Field(None, alias="proxies")
    verify: Optional[Union[bool, str]] = Field(None, alias="verify")
    stream: Optional[bool] = Field(None, alias="stream")
    cert: Optional[Union[str, Tuple[str, str]]] = Field(None, alias="cert")
    
    def __init__(self, *args, **kwargs) -> 'HttpRequest':
        super().__init__(*args, **kwargs)


class HttpClient(EasyModel):
    """
    A simple rate-limited HTTP client for making requests to a REST API.
    """
    config: HttpClientConfig = Field(
        default_factory=HttpClientConfig, alias="config")
    rate_limiter: Optional[RateLimiter] = Field(None, alias="rate_limiter")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = HttpClientConfig(**kwargs.get("config", {}))
        self.rate_limiter = RateLimiter(max_calls=self.config.ratelimit_max_calls, period=self.config.ratelimit_period)
        
    @computed_field
    @property
    def max_calls(self) -> int:
        """
        This property passthrough allows the ratelimit decorator to work successfully
        """
        return self.config.ratelimit_max_calls

    @computed_field
    @property
    def period(self) -> int:
        """
        This property passthrough allows the ratelimit decorator to work successfully.
        """
        return self.config.ratelimit_period

    def _create_absolute_url(self, relative: str) -> str:
        return f"{self.config.base_url}/{relative}"

    @rate_limit()
    @retry_on_error(Type[requests.HTTPError], Type[requests.ConnectionError], Type[requests.Timeout])
    def api_request(self, endpoint: HttpUrl, method: HttpRequestMethod, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        http_obj = HttpRequest.from_dict(data=kwargs, exclude=["method", "url"])
        http_obj.url = self._create_absolute_url(endpoint)
        response = requests.request(method.value, http_obj.url, **(http_obj.to_dict(exlude=["method", "url"])))
        if response.status_code != 200:
            raise requests.HTTPError
        return response.json()

    @rate_limit_async()
    @retry_on_error_async(Type[aiohttp.ClientConnectorError], Type[aiohttp.ClientResponseError], Type[aiohttp.ClientPayloadError])
    async def api_request_async(self, endpoint: HttpUrl, method: HttpRequestMethod, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        http_obj = HttpRequest.from_dict(data=kwargs, exclude=["method", "url"])
        http_obj.url = self._create_absolute_url(endpoint)
        async with aiohttp.ClientSession() as session:
            async with session.request(method.value, http_obj.url, **kwargs) as response:
                if response.status != 200:
                    raise aiohttp.ClientResponseError(request_info=response.request_info, history=response.history, status=response.status, message=response.reason, headers=response.headers)
                return await response.json()
