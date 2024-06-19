import json
import os
from typing import Optional
from anyio import Path
from pydantic import Field
from .easymodel import EasyModel
from pathlib import Path


class DexscreenerConfig(EasyModel):
    """
    Configuration for the Dexscreener class.
    """
    api_key: Optional[str] = Field(None, alias="api_key")


class BirdeyeConfig(EasyModel):
    """
    Configuration for the Birdeye class.
    """
    api_key: Optional[str] = Field(None, alias="api_key")


class AppConfig(EasyModel):
	"""
	Application configuration model.
	"""
	dexscreener: DexscreenerConfig = Field(
		default_factory=DexscreenerConfig, alias="dexscreener")
	birdeye: BirdeyeConfig = Field(
		default_factory=BirdeyeConfig, alias="birdeye")

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.dexscreener = DexscreenerConfig(**kwargs.get("dexscreener", {}))
		self.birdeye = BirdeyeConfig(**kwargs.get("birdeye", {}))
		pass

	def load_config(self, path: Path | str) -> None:
		if isinstance(path, str):
			b_path = Path(path)
		else:
			b_path = path
		if os.path.exists(b_path):
			try:
				with open(b_path, "r") as f:
					config = json.loads(f.read())
					for field_name, field in self.model_fields.items():
						field_type = self.__annotations__[field_name]
						field_value = config.get(field.alias, {})
						if issubclass(field_type, EasyModel):
							setattr(self, field_name, field_type(**field_value))
						else:
							setattr(self, field_name, field_value)
			except Exception as e:
				print(f"Failed to load configuration from file: {e}")	
		else:	
			print(f"Configuration file not found: {b_path}")
		pass