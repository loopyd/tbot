from src.birdeye.models import BirdEyeResponse, SupportedNetworks, DefiNetwork

def test_birdeye_response_model():
    response = BirdEyeResponse(data={"key": "value"}, success=True)
    assert response.data["key"] == "value"
    assert response.success

def test_supported_networks_model():
    supported_networks = SupportedNetworks(data=["solana", "ethereum"])
    assert supported_networks[0] == DefiNetwork.SOLANA
    assert supported_networks[1] == DefiNetwork.ETHEREUM
