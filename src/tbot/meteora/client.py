"""
This module contains the MeteoraClient class that interacts with the Meteora API.
"""
from typing import Any, List, Optional
import aiohttp
from pydantic import Field
from ..common.httpclient import HttpClient
from .models import (
    PairInfo,
    AllGroupOfPairs,
    AllPairsWithPagination,
    BinTradeVolume,
    PairFeeBps,
    PairOrderType,
    PairSortType,
    PairTradeVolume,
    PairTvlSnapshotByDay,
    Swap,
    PositionWithApy,
    WalletEarning,
)
from ..common.easymodel import EasyModel


class MeteoraClient(EasyModel):
    """
    Meteora API HTTP client class that interacts with the Meteora API.
    """
    client: HttpClient = Field(default=..., alias="client")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        self.client: HttpClient = HttpClient()

    async def fetch(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[Any, Any]:
        """
        Fetch data from the Meteora API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url=endpoint, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def get_all_pairs(self) -> List[PairInfo]:
        """
        Get all DLMM pairs with their information.
        """
        endpoint = "/pair/all"
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint)
        return [PairInfo(**pair) for pair in response]

    async def get_all_pairs_by_groups(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        skip_size: Optional[int] = None,
        pools_to_top: Optional[List[str]] = None,
        sort_key: Optional[PairSortType] = None,
        order_by: Optional[PairOrderType] = None,
        search_term: Optional[str] = None,
    ) -> AllGroupOfPairs:
        """
        Get all DLMM pairs with their information grouped by pools.
        """
        endpoint = "/pair/all_by_groups"
        params: dict[str, int | List[str] | str | None] = {
            "page": page if page is not None else 0,
            "limit": limit if limit is not None else 50,
            "skip_size": skip_size if skip_size is not None else 0,
            "pools_to_top": pools_to_top if pools_to_top is not None else [],
            "sort_key": sort_key.value if sort_key is not None else PairSortType.VOLUME.value,
            "order_by": order_by.value if order_by is not None else PairOrderType.DESC.value,
            "search_term": search_term if search_term is not None else "",
        }
        response: dict[str, Any] = await self.fetch(endpoint=endpoint, params=params)
        return AllGroupOfPairs(**response)

    async def get_all_pairs_by_groups_metadata(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        skip_size: Optional[int] = None,
        pools_to_top: Optional[List[str]] = None,
        sort_key: Optional[str] = None,
        order_by: Optional[str] = None,
        search_term: Optional[str] = None,
    ) -> AllGroupOfPairs:
        """
        Get all DLMM pairs with their information grouped by pools with metadata.
        """
        endpoint = "/pair/all_by_groups_metadata"
        params: dict[str, int | List[str] | str | None] = {
            "page": page if page is not None else 0,
            "limit": limit if limit is not None else 50,
            "skip_size": skip_size if skip_size is not None else 0,
            "pools_to_top": pools_to_top if pools_to_top is not None else [],
            "sort_key": sort_key if sort_key is not None else PairSortType.VOLUME.value,
            "order_by": order_by if order_by is not None else PairOrderType.DESC.value,
            "search_term": search_term if search_term is not None else "",
        }
        response: dict[str, Any] = await self.fetch(endpoint=endpoint, params=params)
        return AllGroupOfPairs(**response)

    async def get_all_pairs_with_pagination(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        skip_size: Optional[int] = None,
        pools_to_top: Optional[List[str]] = None,
        sort_key: Optional[str] = None,
        order_by: Optional[str] = None,
        search_term: Optional[str] = None,
    ) -> AllPairsWithPagination:
        """
        Get all DLMM pairs with their information with pagination
        """
        endpoint = "/pair/all_with_pagination"
        params: dict[str, int | List[str] | str | None] = {
            "page": page if page is not None else 0,
            "limit": limit if limit is not None else 50,
            "skip_size": skip_size if skip_size is not None else 0,
            "pools_to_top": pools_to_top if pools_to_top is not None else [],
            "sort_key": sort_key if sort_key is not None else PairSortType.VOLUME.value,
            "order_by": order_by if order_by is not None else PairOrderType.DESC.value,
            "search_term": search_term if search_term is not None else "",
        }
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint, params=params)
        return AllPairsWithPagination(**response)

    async def get_pair_info(self, pair_address: str) -> PairInfo:
        """
        Get information about a specific DLMM pair.
        """
        endpoint: str = f"/pair/{pair_address}"
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint)
        return PairInfo(**response)

    async def get_bin_trade_volume_by_days(
        self,
        pair_address: Optional[str] = None,
        num_of_days: Optional[int] = None
    ) -> List[BinTradeVolume]:
        """
        Get bin trade volume by days.
        """
        endpoint: str = f"/pair/{pair_address}/analytic/bin_trade_volume"
        params: dict[str, int | List[str] | str | None] = {
            "num_of_days": num_of_days if num_of_days is not None else 30,
        }
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint, params=params)
        return [BinTradeVolume(**item) for item in response]

    async def get_pair_fee_bps_by_days(
        self,
        pair_address: Optional[str] = None,
        num_of_days: Optional[int] = None
    ) -> List[PairFeeBps]:
        """
        Get pair fee basis points by days.
        """
        endpoint: str = f"/pair/{pair_address}/analytic/pair_fee_bps"
        params: dict[str, int | List[str] | str | None] = {
            "num_of_days": num_of_days if num_of_days is not None else 30,
        }
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint, params=params)
        return [PairFeeBps(**item) for item in response]

    async def get_pair_daily_trade_volume_by_days(
        self,
        pair_address: Optional[str] = None,
        num_of_days: Optional[int] = None
    ) -> List[PairTradeVolume]:
        """
        Get pair daily trade volume by days.
        """
        endpoint: str = f"/pair/{pair_address}/analytic/pair_trade_volume"
        params: dict[str, int | List[str] | str | None] = {
            "num_of_days": num_of_days if num_of_days is not None else 30,
        }
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint, params=params)
        return [PairTradeVolume(**item) for item in response]

    async def get_pair_tvl_by_days(
        self,
        pair_address: Optional[str] = None,
        num_of_days: Optional[int] = None
    ) -> List[PairTvlSnapshotByDay]:
        """
        Get pair TVL by days.
        """
        endpoint: str = f"/pair/{pair_address}/analytic/pair_tvl"
        params: dict[str, int | List[str] | str | None] = {
            "num_of_days": num_of_days if num_of_days is not None else 30,
        }
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint, params=params)
        return [PairTvlSnapshotByDay(**item) for item in response]

    async def get_pair_swap_records(
        self,
        pair_address: Optional[str] = None,
        rows_to_take: Optional[int] = None
    ) -> List[Swap]:
        """
        Get pair swap records.
        """
        endpoint: str = f"/pair/{pair_address}/analytic/swap_history"
        params: dict[str, int | List[str] | str | None] = {
            "rows_to_take": rows_to_take if rows_to_take is not None else 100
        }
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint, params=params)
        return [Swap(**item) for item in response]

    async def get_position_info(
        self,
        position_address: Optional[str] = None
    ) -> PositionWithApy:
        """
        Get information about a specific DLMM position.
        """
        endpoint: str = f"/position/{position_address}"
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint)
        return PositionWithApy(**response)

    async def get_wallet_earning(
        self,
        wallet_address: Optional[str] = None,
        pair_address: Optional[str] = None
    ) -> List[WalletEarning]:
        """
        Get wallet earning information.
        """
        endpoint: str = f"/wallet/{wallet_address}/{pair_address}/earning"
        response: dict[Any, Any] = await self.fetch(endpoint=endpoint)
        return [WalletEarning(**item) for item in response]
