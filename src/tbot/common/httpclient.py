"""
This module contains a simple rate-limited HTTP client for making requests to a REST API.
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Type, Union
import requests
import aiohttp
from pydantic import Field, HttpUrl

from .retry import retry_on_error, retry_on_error_async
from .ratelimit import RateLimiter, rate_limit, rate_limit_async
from .easymodel import EasyModel


class HttpRequestMethod(Enum):
    """
    Enum class for HTTP request methods.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpClientConfig(EasyModel):
    """
    Configuration for the Rate-Limited HttpClient class.
    """
    base_url: HttpUrl = Field(
        default="https://api.dexscreener.io/latest", alias="base_url")
    ratelimit_max_calls: int = Field(default=300, alias="ratelimit_max_calls")
    ratelimit_period: int = Field(default=60, alias="ratelimit_period")


class HttpRequest(EasyModel):
    """
    Model class for HTTP requests.
    """
    url: Optional[Union[HttpUrl, str]] = Field(default=None, alias="url")
    method: Optional[HttpRequestMethod] = Field(
        default=HttpRequestMethod.GET, alias="method")
    params: Optional[Union[Dict[str, Any], List[Tuple[str, Any]], bytes]] = Field(
        default=None, alias="params")
    data: Optional[Union[Dict[str, Any], List[Tuple[str, Any]],
                         bytes, Any]] = Field(default=None, alias="data")
    body: Optional[Any] = Field(default=None, alias="body")
    headers: Optional[Dict[str, str]] = Field(default=None, alias="headers")
    cookies: Optional[Union[Dict[str, str], Any]
                      ] = Field(default=None, alias="cookies")
    files: Optional[Dict[str, Union[Any, Tuple[str, Any, Optional[str],
                                               Optional[Dict[str, str]]]]]] = Field(default=None, alias="files")
    auth: Optional[Union[Tuple[str, str], Any]
                   ] = Field(default=None, alias="auth")
    timeout: Optional[Union[float, Tuple[float, float]]
                      ] = Field(default=None, alias="timeout")
    allow_redirects: Optional[bool] = Field(
        default=None, alias="allow_redirects")
    proxies: Optional[Dict[str, str]] = Field(default=None, alias="proxies")
    verify: Optional[Union[bool, str]] = Field(default=None, alias="verify")
    stream: Optional[bool] = Field(default=None, alias="stream")
    cert: Optional[Union[str, Tuple[str, str]]
                   ] = Field(default=None, alias="cert")


class HttpClient(EasyModel):
    """
    A simple rate-limited HTTP client for making requests to a REST API.
    """
    config: HttpClientConfig = Field(
        default_factory=HttpClientConfig, alias="config")
    rate_limiter: Optional[RateLimiter] = Field(None, alias="rate_limiter")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.config = HttpClientConfig(**kwargs.get("config", {}))
        self.rate_limiter = RateLimiter(
            max_calls=self.config.ratelimit_max_calls, period=self.config.ratelimit_period)

    @property
    def max_calls(self) -> int:
        """
        This property passthrough allows the ratelimit decorator to work successfully
        """
        return self.config.ratelimit_max_calls

    @property
    def period(self) -> int:
        """
        This property passthrough allows the ratelimit decorator to work successfully.
        """
        return self.config.ratelimit_period

    def _create_absolute_url(self, relative: HttpUrl) -> str:
        return f"{self.config.base_url}/{relative}"

    @rate_limit()
    @retry_on_error(requests.HTTPError, requests.ConnectionError, requests.Timeout)
    def api_request(
        self,
        endpoint: HttpUrl,
        method: HttpRequestMethod,
        **kwargs: Any
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make an API request to the specified endpoint.
        """
        http_obj = HttpRequest.from_dict(
            data=kwargs, exclude=["method", "url"])
        http_obj.url = HttpUrl(self._create_absolute_url(relative=endpoint))
        response: requests.Response = requests.request(
            method=method.value, url=http_obj.url, **(http_obj.to_dict(exclude=["method", "url"])))
        if response.status_code != 200:
            raise requests.HTTPError
        return response.json()

    @rate_limit_async()
    @retry_on_error_async(
        Type[aiohttp.ClientConnectorError],
        Type[aiohttp.ClientResponseError],
        Type[aiohttp.ClientPayloadError]
    )
    async def api_request_async(
        self,
        endpoint: HttpUrl,
        method: HttpRequestMethod,
        **kwargs: Any
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make an API request to the specified endpoint asynchronously.
        """
        http_obj = HttpRequest.from_dict(
            data=kwargs, exclude=["method", "url"])
        http_obj.url = self._create_absolute_url(relative=endpoint)
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method.value, url=http_obj.url, **kwargs) as response:
                if response.status != 200:
                    raise aiohttp.ClientResponseError(request_info=response.request_info, history=response.history,
                                                      status=response.status, message=str(object=response.reason), headers=response.headers)
                return await response.json()
