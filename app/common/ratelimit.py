"""
ratelimit.py - A rate limiter that can be used as a context manager or decorator.
"""
import asyncio
import collections
import time
from typing import Callable, Any, Optional
from functools import wraps
from pydantic import Field, SkipValidation, computed_field
from .easymodel import EasyModel


class RateLimiter(EasyModel):
    """
    A rate limiter that can be used as a context manager or decorator.
    """
    calls: collections.deque = Field(
        default_factory=collections.deque, alias='calls')
    max_calls: int = Field(default_factory=int, alias='max_calls')
    period: float = Field(default_factory=float, alias='period')
    sync_lock: asyncio.Lock = Field(default_factory=asyncio.Lock, alias='sync_lock')
    async_lock: asyncio.Lock = Field(default_factory=asyncio.Lock, alias='async_lock')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_calls = kwargs.get('max_calls', 300)
        self.period = kwargs.get('period', 60)
        pass

    def __enter__(self) -> 'RateLimiter':
        with self.sync_lock:
            sleep_time = self.get_sleep_time()
            if sleep_time > 0:
                time.sleep(sleep_time)
            return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        with self.sync_lock:
            self._clear_calls()

    async def __aenter__(self) -> 'RateLimiter':
        async with self.async_lock:
            sleep_time = self.get_sleep_time()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        async with self.async_lock:
            self._clear_calls()

    def get_sleep_time(self) -> float:
        if len(self.calls) >= self.max_calls:
            until = self.calls[0] + self.period
            return until - time.time()
        return 0

    def _clear_calls(self) -> None:
        self.calls.append(time.time())
        while self.calls and (time.time() - self.calls[0]) >= self.period:
            self.calls.popleft()

    @computed_field
    @property
    def timespan(self) -> float:
        return time.time() - self.calls[0] if self.calls else 0


def rate_limit_async(max_calls: Optional[int] = None, period: Optional[float] = None):
    """
    An asyncronous decorator that limits the number of times a coroutine can be called
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            limiter = RateLimiter(
                max_calls=max_calls or self.max_calls,
                period=period or self.period
            )
            async with limiter:
                return await func(self, *args, **kwargs)
        return wrapper
    return decorator


def rate_limit(max_calls: Optional[int] = None, period: Optional[float] = None):
    """
    A synchronous decorator that limits the number of times a function can be called
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            limiter = RateLimiter(
                max_calls=max_calls or self.max_calls,
                period=period or self.period
            )
            with limiter:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator
