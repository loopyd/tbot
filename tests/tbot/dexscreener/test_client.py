import asyncio
import pytest
from tbot.dexscreener.client import DexscreenerClient
from tbot.dexscreener.models import DefiNetwork


@pytest.fixture
def dexscreener_client():
    return DexscreenerClient(api_key="test_key")


def test_get_pairs_async(dexscreener_client, mocker):
    mock_response = mocker.patch('app.httpclient.HttpClient.api_request_async')
    mock_response.return_value = {
        "data": [{"base_token": {"symbol": "SOL"}, "quote_token": {"symbol": "USDC"}}]}

    async def test():
        pairs = await dexscreener_client.get_pairs_async("address", DefiNetwork.SOLANA)
        assert pairs.base_token.symbol == "SOL"
        assert pairs.quote_token.symbol == "USDC"

    asyncio.run(test())


@pytest.mark.asyncio
async def test_get_pairs_async_with_asyncio(dexscreener_client, mocker):
    mock_response = mocker.patch('app.httpclient.HttpClient.api_request_async')
    mock_response.return_value = {
        "data": [{"base_token": {"symbol": "SOL"}, "quote_token": {"symbol": "USDC"}}]}

    pairs = await dexscreener_client.get_pairs_async("address", DefiNetwork.SOLANA)
    assert pairs.base_token.symbol == "SOL"
    assert pairs.quote_token.symbol == "USDC"
