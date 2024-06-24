"""
Python module for retrying a function call if an exception is raised.
"""
import asyncio
from functools import wraps
import time
from typing import Any, Callable, Optional, Type

from .ratelimit import RateLimiter


def retry_on_error(
    *exceptions: Type[Exception],
    max_retries: Optional[int] = None,
    delay: Optional[float] = None,
    backoff: Optional[float] = None,
) -> Callable[..., Any]:
    """
    A decorator that retries a function call if the registered exceptions are raised.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            b_current_retries = 0
            b_max_retries: int | Any = max_retries if max_retries is not None else getattr(
                self, "max_retries", 3)
            b_delay: float | Any = delay if delay is not None else getattr(
                self, "delay", 1.0)
            b_backoff: float | Any = backoff if backoff is not None else getattr(
                self, "backoff", 2.0)
            b_exceptions: Any = exceptions if exceptions else (
                NotImplementedError,)

            while b_current_retries < b_max_retries:
                try:
                    with RateLimiter(max_calls=getattr(self, "max_calls", 300), period=getattr(self, "period", 60)):
                        result = func(self, *args, **kwargs)
                        return result
                except Exception as e:
                    b_current_retries += 1
                    if b_current_retries >= b_max_retries:
                        raise e
                    time.sleep(
                        b_delay * (b_backoff ** (b_current_retries - 1)))

        return wrapper

    return decorator


def retry_on_error_async(
    *exceptions: Type[Exception],
    max_retries: Optional[int] = None,
    delay: Optional[float] = None,
    backoff: Optional[float] = None,
) -> Callable[..., Any]:
    """
    A decorator that retries a function call if the registered exceptions are raised.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=func)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            b_current_retries = 0
            b_max_retries: int | Any = max_retries if max_retries is not None else getattr(
                self, "max_retries", 3)
            b_delay: float | Any = delay if delay is not None else getattr(
                self, "delay", 1.0)
            b_backoff: float | Any = backoff if backoff is not None else getattr(
                self, "backoff", 2.0)
            b_exceptions: Any = exceptions if exceptions else (
                NotImplementedError,)

            while b_current_retries < b_max_retries:
                try:
                    async with RateLimiter(
                        max_calls=getattr(self, "max_calls", 300), period=getattr(self, "period", 60)
                    ):
                        result = await func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    b_current_retries += 1
                    if b_current_retries >= b_max_retries:
                        raise e
                    await asyncio.sleep(delay=b_delay * (b_backoff ** (b_current_retries - 1)))

        return wrapper

    return decorator
