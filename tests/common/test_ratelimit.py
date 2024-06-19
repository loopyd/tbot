import pytest
import asyncio
from src.common.ratelimit import RateLimiter

@pytest.fixture
def rate_limiter():
    return RateLimiter(max_calls=2, period=1)

def test_rate_limiter(rate_limiter):
    with rate_limiter:
        pass

    with rate_limiter:
        pass

    with pytest.raises(Exception):
        with rate_limiter:
            pass

@pytest.mark.asyncio
async def test_rate_limiter_async(rate_limiter):
    async with rate_limiter:
        pass

    async with rate_limiter:
        pass

    with pytest.raises(Exception):
        async with rate_limiter:
            pass
