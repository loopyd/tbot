"""
This module contains the configuration models for the application.
"""
import json
import os
from typing import Any, Optional
from pydantic import Field
from pathlib import Path

from .easymodel import EasyModel


class DexscreenerConfig(EasyModel):
    """
    Configuration for the Dexscreener class.
    """
    api_key: Optional[str] = Field(default=None, alias="api_key")


class BirdeyeConfig(EasyModel):
    """
    Configuration for the Birdeye class.
    """
    api_key: Optional[str] = Field(default=None, alias="api_key")


class AppConfig(EasyModel):
    """
    Application configuration model.
    """
    dexscreener: DexscreenerConfig = Field(
        default_factory=DexscreenerConfig, alias="dexscreener")
    birdeye: BirdeyeConfig = Field(
        default_factory=BirdeyeConfig, alias="birdeye")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        self.dexscreener = DexscreenerConfig(**kwargs.get("dexscreener", {}))
        self.birdeye = BirdeyeConfig(**kwargs.get("birdeye", {}))

    def load_config(self, path: Path | str) -> None:
        """
        Load configuration from a file.
        """
        if isinstance(path, str):
            b_path = Path(path)
        else:
            b_path = path
        if os.path.exists(path=b_path):
            try:
                with open(file=b_path, mode='r', encoding='utf-8') as f:
                    config: Any = json.loads(f.read())
                    for field_name, field in self.model_fields.items():
                        field_type: Any = self.__annotations__[field_name]
                        field_value: Any = config.get(field.alias, {})
                        if issubclass(field_type, EasyModel):
                            setattr(self, field_name,
                                    field_type(**field_value))
                        else:
                            setattr(self, field_name, field_value)
            except Exception as e:
                print(f"Failed to load configuration from file: {e}")
        else:
            print(f"Configuration file not found: {b_path}")
