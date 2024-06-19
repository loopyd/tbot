from src.dexscreener.models import TokenPair

def test_token_pair_model():
    token_pair = TokenPair(base_token={"symbol": "SOL"}, quote_token={"symbol": "USDC"})
    assert token_pair.base_token.symbol == "SOL"
    assert token_pair.quote_token.symbol == "USDC"
