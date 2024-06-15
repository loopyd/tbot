import asyncio
import sys
from typing import List

from .dex.client import DexscreenerClient


async def main(args: List[str]) -> None:
	"""
	Main entrypoint for the application.
	"""
	dex_client = DexscreenerClient()
	result = await dex_client.search_pairs_async("AA")
	for pair in result:
		print(f"Pair: {pair.base_token.name} ({pair.base_token.symbol}) / {pair.quote_token.name} ({pair.quote_token.symbol})")
	pass

if __name__ == "__main__":
	asyncio.run(main(sys.argv[1:]))