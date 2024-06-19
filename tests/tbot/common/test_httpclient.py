import requests
import pytest
from tbot.common.httpclient import HttpClient, HttpRequestMethod


@pytest.fixture
def http_client():
    return HttpClient()


def test_api_request(http_client, mocker):
    mock_response = mocker.patch('requests.request')
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"key": "value"}

    response = http_client.api_request("test", HttpRequestMethod.GET)
    assert response == {"key": "value"}


def test_api_request_error(http_client, mocker):
    mock_response = mocker.patch('requests.request')
    mock_response.return_value.status_code = 404

    with pytest.raises(requests.HTTPError):
        http_client.api_request("test", HttpRequestMethod.GET)
