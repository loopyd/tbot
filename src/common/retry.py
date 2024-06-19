import asyncio
from functools import wraps
from re import T
import time
from typing import Any, Callable, List, Optional, Tuple, Type

from .ratelimit import RateLimiter


def retry_on_error(*exceptions, max_retries: Optional[int] = None, delay: Optional[float] = None, backoff: Optional[float] = None) -> Callable[..., Any]:
	"""
	A decorator that retries a function call if the registered exceptions are raised.
	"""
	def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			b_current_retries = 0
			b_max_retries = max_retries if max_retries is not None else getattr(
				self, 'max_retries', 3)
			b_delay = delay if delay is not None else getattr(
				self, 'delay', 1.0)
			b_backoff = backoff if backoff is not None else getattr(
				self, 'backoff', 2.0)
			b_exceptions = exceptions if exceptions else (NotImplementedError,)

			while b_current_retries < b_max_retries:
				try:
					with RateLimiter(max_calls=getattr(self, 'max_calls', 300), period=getattr(self, 'period', 60)):
						result = func(self, *args, **kwargs)
						return result
				except Exception as e:
					b_current_retries += 1
					if b_current_retries >= b_max_retries:
						raise e
					time.sleep(b_delay * (b_backoff ** (b_current_retries - 1)))
		return wrapper
	return decorator

def retry_on_error_async(*exceptions, max_retries: Optional[int] = None, delay: Optional[float] = None, backoff: Optional[float] = None) -> Callable[..., Any]:
	"""
	A decorator that retries a function call if the registered exceptions are raised.
	"""
	def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
		@wraps(func)
		async def wrapper(self, *args, **kwargs):
			b_current_retries = 0
			b_max_retries = max_retries if max_retries is not None else getattr(self, 'max_retries', 3)
			b_delay = delay if delay is not None else getattr(self, 'delay', 1.0)
			b_backoff = backoff if backoff is not None else getattr(self, 'backoff', 2.0)
			b_exceptions = exceptions if exceptions else (NotImplementedError,)

			while b_current_retries < b_max_retries:
				try:
					async with RateLimiter(max_calls=getattr(self, 'max_calls', 300), period=getattr(self, 'period', 60)):
						result = await func(self, *args, **kwargs)
					return result
				except Exception as e:
					b_current_retries += 1
					if b_current_retries >= b_max_retries:
						raise e
					await asyncio.sleep(b_delay * (b_backoff ** (b_current_retries - 1)))
		return wrapper
	return decorator