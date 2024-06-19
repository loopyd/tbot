import asyncio
import sys
from typing import List, Optional, Union
from anyio import Path

from .dexscreener.models import TokenPair

from .birdeye.models import DefiNetwork
from .common.config import AppConfig
from .birdeye.client import BirdeyeClient
from .dexscreener.client import DexscreenerClient


async def main_async(args: Optional[List[str]] = None) -> None:
	"""
	Main entry point for the application.
	"""
	app_config = AppConfig()
	app_config.load_config(Path(sys.argv[0]).parent.joinpath("config.json"))
	dex_client = DexscreenerClient()
	birdeye_client = BirdeyeClient(api_key=app_config.birdeye.api_key)

	# supported = await birdeye_client.get_supported_networks_async()
	SOL_BASE = "So11111111111111111111111111111111111111112"
	SOL_USDC = "FpCMFDFGYotvufJ7HrFHsWEiiQCGbkLCtwHiDnh7o28Q"
	price = await birdeye_client.get_price_async(address=SOL_BASE, network=DefiNetwork.SOLANA)
	token: Union[TokenPair, List[TokenPair], None] = await dex_client.get_pairs_async(address=SOL_USDC, network=DefiNetwork.SOLANA)
	print(f"{token.base_token.name} ({token.base_token.symbol}) | Price: {price.value} {token.quote_token.symbol} on {price.updateHumanTime}")


def main(args: Optional[List[str]] = None) -> None:
	asyncio.run(main_async(args))
 
 
if __name__ == "__main__":
    main(sys.argv[1:])
