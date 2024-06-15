import asyncio
from itertools import product
import sys
from typing import List

from .dexscreener.client import DexscreenerClient


async def search_pairs_async(dex_client: DexscreenerClient, search: str, result_queue: asyncio.Queue, semaphore: asyncio.Semaphore) -> None:
	"""
	Search for pairs asynchronously and put unique results into the result queue.
	"""
	b_result = await dex_client.search_pairs_async(search_query=f"{search}")
	if len(b_result) > 0:
		await result_queue.put((search, b_result))
	else:
		await result_queue.put((search, []))
	


async def process_results(result_queue: asyncio.Queue, result: List) -> None:
	"""
	Process results from the result queue and append unique pairs to the result list.
	"""
	while True:
		search, b_result = await result_queue.get()
		if search is None:
			break
		size_before = len(result)
		for pair in b_result:
			if pair not in result:
				result.append(pair)
		size_after = len(result)
		print("S: {0:5} V: {1:5} P: {2:5}\r".format(search, size_after - size_before, size_after), end="")
		result_queue.task_done()


async def generate_search_queries(queue: asyncio.Queue) -> None:
	"""
	Generate search queries and put them in the queue.
	"""
	for e in range(2, 5):
		for p in product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=e):
			await queue.put(''.join(p))
			await asyncio.sleep(0.1)
	await queue.put(None)
	print("Search query generation complete")


async def main(args: List[str]) -> None:
	"""
	Main entry point for the application.
	"""
	dex_client = DexscreenerClient()
	search_queue = asyncio.Queue()
	result_queue = asyncio.Queue()
	search_sephamore = asyncio.Semaphore(1)
	result = []
	tasks = [
		asyncio.create_task(generate_search_queries(search_queue)),
		asyncio.create_task(process_results(result_queue, result)),
	]
	while True:
		search = await search_queue.get()
		if search is None:
			break
		tasks.append(asyncio.create_task(search_pairs_async(
			dex_client, search, result_queue, search_sephamore)))

	print("Processing search queries...")
	await asyncio.gather(*tasks)
	print(f"Final result count: {len(result)}")

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
