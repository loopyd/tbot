import pytest
import asyncio
from src.common.retry import retry_on_error, retry_on_error_async

class TestRetry:
    def __init__(self):
        self.attempts = 0

    @retry_on_error(ValueError, max_retries=3, delay=0.1)
    def test_func(self):
        self.attempts += 1
        if self.attempts < 3:
            raise ValueError("Error")
        return "Success"

    @retry_on_error_async(ValueError, max_retries=3, delay=0.1)
    async def test_func_async(self):
        self.attempts += 1
        if self.attempts < 3:
            raise ValueError("Error")
        return "Success"

def test_retry():
    obj = TestRetry()
    result = obj.test_func()
    assert result == "Success"
    assert obj.attempts == 3

@pytest.mark.asyncio
async def test_retry_async():
    obj = TestRetry()
    result = await obj.test_func_async()
    assert result == "Success"
    assert obj.attempts == 3
