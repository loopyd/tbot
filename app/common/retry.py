import asyncio
from functools import wraps
import time
from typing import Any, Callable, List, Optional, Tuple, Type


def retry_on_error(*exceptions: Tuple[Type[Exception]], max_retries: Optional[int] = None, delay: Optional[float] = None, backoff: Optional[float] = None) -> Callable[..., Any]:
    """
    A decorator that retries a function call if the registered exceptions are raised.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            b_current_retries, b_max_retries, b_delay, b_backoff, b_exceptions = (
                0,
                max_retries if max_retries is not None else getattr(self, 'max_retries') if hasattr(self, "max_retries") else 3,
                delay if delay is not None else getattr(self, 'delay') if hasattr(self, "delay") else 1.0,
                backoff if backoff is not None else getattr(self, 'backoff') if hasattr(self, "backoff") else 2.0,
                list(*exceptions) if exceptions else (NotImplementedError,),
            )
            while b_current_retries < b_max_retries:
                try:
                    result = func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    if not type(e) in b_exceptions:
                        raise e
                    b_current_retries += 1
                    if b_current_retries >= b_max_retries:
                        raise e
                    time.sleep(b_delay * (b_backoff ** (b_max_retries - 1)))
        return wrapper
    return decorator


def retry_on_error_async(*exceptions: Tuple[Type[Exception]], max_retries: Optional[int] = None, delay: Optional[float] = None, backoff: Optional[float] = None):
    """
    A decorator that retries a function call if the registered exceptions are raised.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            b_current_retries, b_max_retries, b_delay, b_backoff, b_exceptions = (
                0,
                max_retries if max_retries is not None else getattr(self, 'max_retries') if hasattr(self, "max_retries") else 3,
                delay if delay is not None else getattr(self, 'delay') if hasattr(self, "delay") else 1.0,
                backoff if backoff is not None else getattr(self, 'backoff') if hasattr(self, "backoff") else 2.0,
            	exceptions if exceptions else (NotImplementedError,),
            )
            while b_current_retries < b_max_retries:
                try:
                    result = await func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    if not type(e) in b_exceptions:
                        raise e
                    b_current_retries += 1
                    if b_current_retries >= b_max_retries:
                        raise e
                    await asyncio.sleep(b_delay * (b_backoff ** (b_max_retries - 1)))
        return wrapper
    return decorator