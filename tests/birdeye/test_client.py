import asyncio
import pytest
from src.birdeye.client import BirdeyeClient
from src.birdeye.models import DefiNetwork

@pytest.fixture
def birdeye_client():
    return BirdeyeClient(api_key="test_key")

def test_get_price_async(birdeye_client, mocker):
    mock_response = mocker.patch('app.httpclient.HttpClient.api_request_async')
    mock_response.return_value = {"data": {"value": 100.0, "updateUnixTime": 1633024800}}

    async def test():
        price = await birdeye_client.get_price_async("address", DefiNetwork.SOLANA)
        assert price.value == 100.0
        assert price.updateHumanTime == "09-30-2021 @ 17:00:00 PM (UTC)"

    asyncio.run(test())

@pytest.mark.asyncio
async def test_get_price_async_with_asyncio(birdeye_client, mocker):
    mock_response = mocker.patch('app.httpclient.HttpClient.api_request_async')
    mock_response.return_value = {"data": {"value": 100.0, "updateUnixTime": 1633024800}}

    price = await birdeye_client.get_price_async("address", DefiNetwork.SOLANA)
    assert price.value == 100.0
    assert price.updateHumanTime == "09-30-2021 @ 17:00:00 PM (UTC)"
