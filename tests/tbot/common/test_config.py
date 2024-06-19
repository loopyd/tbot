import json
import pytest
from tbot.common.config import AppConfig


@pytest.fixture
def config_file(tmp_path):
    config_path = tmp_path / "config.json"
    config_content = {
        "dexscreener": {"api_key": "dex_api_key"},
        "birdeye": {"api_key": "birdeye_api_key"}
    }
    config_path.write_text(json.dumps(config_content))
    return config_path


def test_load_config(config_file):
    app_config = AppConfig()
    app_config.load_config(config_file)
    assert app_config.dexscreener.api_key == "dex_api_key"
    assert app_config.birdeye.api_key == "birdeye_api_key"


def test_missing_config_file(tmp_path):
    app_config = AppConfig()
    with pytest.raises(FileNotFoundError):
        app_config.load_config(tmp_path / "nonexistent.json")
