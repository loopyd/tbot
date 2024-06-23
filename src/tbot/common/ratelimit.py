"""
ratelimit.py - A rate limiter that can be used as a context manager or decorator.
"""

import asyncio
import collections
import threading
import time
from typing import Callable, Any, Optional
from types import TracebackType
from functools import wraps

from pydantic import Field, SkipValidation
from .easymodel import EasyModel


class RateLimiter(EasyModel):
    """
    A rate limiter that can be used as a context manager or decorator.
    """
    calls: collections.deque = Field(default_factory=collections.deque, alias="calls") # type: ignore
    max_calls: int = Field(default_factory=int, alias="max_calls")
    period: float = Field(default_factory=float, alias="period")
    sync_lock: SkipValidation[threading.RLock] = Field(
        default_factory=SkipValidation[threading.RLock], alias="sync_lock", validate_default=False
    )
    async_lock: asyncio.Lock = Field(
        default_factory=asyncio.Lock, alias="async_lock")
    min_interval: float = Field(default_factory=float, alias="min_interval")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.max_calls = kwargs.get("max_calls", self.max_calls)
        self.period = kwargs.get("period", self.period)
        self.min_interval = self.period / self.max_calls

    def __enter__(self) -> "RateLimiter":
        with self.sync_lock:
            self._ensure_rate_limit()
            return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        with self.sync_lock:
            self._record_call()

    async def __aenter__(self) -> "RateLimiter":
        async with self.async_lock:
            await self._ensure_rate_limit_async()
            return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        async with self.async_lock:
            self._record_call()

    def _ensure_rate_limit(self) -> None:
        sleep_time: float = self._get_sleep_time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            time.sleep(self.min_interval)

    async def _ensure_rate_limit_async(self) -> None:
        sleep_time: float = self._get_sleep_time()
        if sleep_time > 0:
            await asyncio.sleep(delay=sleep_time)
        else:
            await asyncio.sleep(delay=self.min_interval)

    def _get_sleep_time(self) -> float:
        self._clear_old_calls()
        if self.calls and len(self.calls) >= self.max_calls:
            elapsed: float = time.time() - self.calls[0]
            sleep_time: float = self.period - elapsed
            if sleep_time > 0:
                return sleep_time
        return 0

    def _record_call(self) -> None:
        self.calls.append(time.time())
        self._clear_old_calls()

    def _clear_old_calls(self) -> None:
        while self.calls and (time.time() - self.calls[0]) >= self.period:
            self.calls.popleft()

    @property
    def timespan(self) -> float:
        return time.time() - self.calls[0] if self.calls else 0


def rate_limit_async(
    max_calls: Optional[int] = None,
    period: Optional[float] = None,
    limiter: Optional[RateLimiter] = None
) -> Callable[..., Callable[..., Any]]:
    """
    An asynchronous decorator that limits the number of times a coroutine can be called
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=func)
        async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            r_limiter: RateLimiter | Any = (
                limiter
                if limiter is not None
                else getattr(
                    self,
                    "rate_limiter",
                    RateLimiter(
                        max_calls=max_calls if max_calls is not None else getattr(
                            self, "max_calls", 100),
                        period=period if period is not None else getattr(
                            self, "period", 60),
                    ),
                )
            )
            async with r_limiter:
                return await func(self, *args, **kwargs)

        return wrapper

    return decorator


def rate_limit(max_calls: Optional[int] = None, period: Optional[float] = None, limiter: Optional[RateLimiter] = None):
    """
    A synchronous decorator that limits the number of times a function can be called
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            r_limiter: RateLimiter | Any = (
                limiter
                if limiter is not None
                else getattr(
                    self,
                    "rate_limiter",
                    RateLimiter(
                        max_calls=max_calls if max_calls is not None else getattr(
                            self, "max_calls", 100),
                        period=period if period is not None else getattr(
                            self, "period", 60),
                    ),
                )
            )
            with r_limiter:
                return func(self, *args, **kwargs)

        return wrapper

    return decorator
