import asyncio
from itertools import product
import sys
from typing import List

from anyio import Path

from .common.config import AppConfig

from .birdeye.client import BirdeyeClient
from .dexscreener.client import DexscreenerClient

async def main(args: List[str]) -> None:
	"""
	Main entry point for the application.
	"""
	app_config = AppConfig()
	app_config.load_config(Path(sys.argv[0]).parent.joinpath("config.json"))
	dex_client = DexscreenerClient()
	birdeye_client = BirdeyeClient(api_key=app_config.birdeye.api_key)
 
	supported = await birdeye_client.get_supported_networks_async()
	print(supported)
 

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
