"""
This module contains the MeteoraClient model and type hints.
"""
from enum import Enum
from typing import List
from pydantic import Field

from ..common.easymodel import EasyModel


class DefiNetwork(Enum):
    """
    Enum class for DeFi networks.
    """
    SOLANA = "solana"
    ETHEREUM = "ethereum"
    ARBITRUM = "arbitrum"
    AVALANCHE = "avalanche"
    BSC = "bsc"
    OPTIMISM = "optimism"
    POLYGON = "polygon"
    BASE = "base"
    ZKSYNC = "zksync"
    SUI = "sui"


class PairSortType(Enum):
    """
    Enum class for DLMM pair sort types.
    """
    TVL = "tvl"
    VOLUME = "volume"
    FEE_TVL_RATIO = "feetvlratio"
    LM = "lm"


class PairOrderType(Enum):
    """
    Enum class for DLMM pair order types.
    """
    ASC = "asc"
    DESC = "desc"


class PairInfo(EasyModel):
    """
    Model class for DLMM pair information.
    """
    address: str = Field(default=..., alias="address")
    name: str = Field(default=..., alias="name")
    mint_x: str = Field(default=..., alias="mint_x")
    mint_y: str = Field(default=..., alias="mint_y")
    reserve_x: str = Field(default=..., alias="reserve_x")
    reserve_x_amount: int = Field(default=..., alias="reserve_x_amount")
    reserve_y: str = Field(default=..., alias="reserve_y")
    reserve_y_amount: int = Field(default=..., alias="reserve_y_amount")
    bin_step: int = Field(default=..., alias="bin_step")
    base_fee_percentage: str = Field(default=..., alias="base_fee_percentage")
    max_fee_percentage: str = Field(default=..., alias="max_fee_percentage")
    protocol_fee_percentage: str = Field(default=..., alias="protocol_fee_percentage")
    liquidity: str = Field(default=..., alias="liquidity")
    reward_mint_x: str = Field(default=..., alias="reward_mint_x")
    reward_mint_y: str = Field(default=..., alias="reward_mint_y")
    fees_24h: float = Field(default=..., alias="fees_24h")
    today_fees: float = Field(default=..., alias="today_fees")
    trade_volume_24h: float = Field(default=..., alias="trade_volume_24h")
    cumulative_trade_volume: float = Field(default=...,
                                           alias="cumulative_trade_volume")
    cumulative_fee_volume: float = Field(default=..., alias="cumulative_fee_volume")
    current_price: float = Field(default=..., alias="current_price")
    apr: float = Field(default=..., alias="apr")
    apy: float = Field(default=..., alias="apy")
    farm_apr: float = Field(default=..., alias="farm_apr")
    farm_apy: float = Field(default=..., alias="farm_apy")
    hide: bool = Field(default=..., alias="hide")


class AllGroupOfPairs(EasyModel):
    """
    Model class for all DLMM pairs.
    """
    groups: List[PairInfo] = Field(default=..., alias="groups")
    total: int = Field(default=..., alias="total")


class AllGroupOfPairsMetadata(EasyModel):
    """
    Model class for all DLMM pairs with metadata.
    """
    metadatas: List[PairInfo] = Field(default=..., alias="metadatas")
    total: int = Field(default=..., alias="total")


class AllPairsWithPagination(EasyModel):
    """
    Model class for all DLMM pairs with pagination.
    """
    pairs: List[PairInfo] = Field(default=..., alias="pairs")
    total: int = Field(default=..., alias="total")


class BinTradeVolume(EasyModel):
    """
    Model class for bin trade volume by days.
    """
    bin_id: int = Field(default=..., alias="bin_id")
    total_amount_y: str = Field(default=..., alias="total_amount_y")
    total_amount_x: str = Field(default=..., alias="total_amount_x")
    total_amount_usd: float = Field(default=..., alias="total_amount_usd")


class PairFeeBps(EasyModel):
    """
    Model class for pair fee basis points.
    """
    pair_address: str = Field(default=..., alias="pair_address")
    min_fee_bps: float = Field(default=..., alias="min_fee_bps")
    max_fee_bps: float = Field(default=..., alias="max_fee_bps")
    average_fee_bps: float = Field(default=..., alias="average_fee_bps")
    hour_date: str = Field(default=..., alias="hour_date")


class PairTradeVolume(EasyModel):
    """
    Model class for pair daily trade volume by days.
    """
    pair_address: str = Field(default=..., alias="pair_address")
    trade_volume: float = Field(default=..., alias="trade_volume")
    fee_volume: float = Field(default=..., alias="fee_volume")
    protocol_fee_volume: float = Field(default=..., alias="protocol_fee_volume")
    day_date: str = Field(default=..., alias="day_date")


class PairTvlSnapshotByDay(EasyModel):
    """
    Model class for pair TVL snapshot by days.
    """
    pair_address: str = Field(default=..., alias="pair_address")
    total_value_locked: float = Field(default=..., alias="total_value_locked")
    day_date: str = Field(default=..., alias="day_date")


class Swap(EasyModel):
    """
    Model class for DLMM pair swap information.
    """
    tx_id: str = Field(default=..., alias="tx_id")
    in_amount: int = Field(default=..., alias="in_amount")
    in_amount_usd: float = Field(default=..., alias="in_amount_usd")
    out_amount: int = Field(default=..., alias="out_amount")
    out_amount_usd: float = Field(default=..., alias="out_amount_usd")
    trade_fee: int = Field(default=..., alias="trade_fee")
    trade_fee_usd: float = Field(default=..., alias="trade_fee_usd")
    protocol_fee: int = Field(default=..., alias="protocol_fee")
    protocol_fee_usd: float = Field(default=..., alias="protocol_fee_usd")
    onchain_timestamp: int = Field(default=..., alias="onchain_timestamp")
    pair_address: str = Field(default=..., alias="pair_address")
    start_bin_id: int = Field(default=..., alias="start_bin_id")
    end_bin_id: int = Field(default=..., alias="end_bin_id")
    bin_count: int = Field(default=..., alias="bin_count")
    fee_bps: float = Field(default=..., alias="fee_bps")
    in_token: str = Field(default=..., alias="in_token")
    out_token: str = Field(default=..., alias="out_token")


class PositionWithApy(EasyModel):
    """
    Model class for DLMM position information with APY.
    """
    address: str = Field(default=..., alias="address")
    pair_address: str = Field(default=..., alias="pair_address")
    owner: str = Field(default=..., alias="owner")
    total_fee_x_claimed: int = Field(default=..., alias="total_fee_x_claimed")
    total_fee_y_claimed: int = Field(default=..., alias="total_fee_y_claimed")
    total_reward_x_claimed: int = Field(default=..., alias="total_reward_x_claimed")
    total_reward_y_claimed: int = Field(default=..., alias="total_reward_y_claimed")
    total_fee_usd_claimed: float = Field(default=..., alias="total_fee_usd_claimed")
    total_reward_usd_claimed: float = Field(default=...,
                                            alias="total_reward_usd_claimed")
    fee_apy_24h: float = Field(default=..., alias="fee_apy_24h")
    fee_apr_24h: float = Field(default=..., alias="fee_apr_24h")
    daily_fee_yield: float = Field(default=..., alias="daily_fee_yield")


class WalletEarning(EasyModel):
    """
    Model class for wallet earning information.
    """
    total_fee_usd_claimed: float = Field(default=..., alias="total_fee_usd_claimed")
    total_fee_x_claimed: str = Field(default=..., alias="total_fee_x_claimed")
    total_fee_y_claimed: str = Field(default=..., alias="total_fee_y_claimed")
    total_reward_usd_claimed: float = Field(default=...,
                                            alias="total_reward_usd_claimed")
    total_reward_x_claimed: str = Field(default=..., alias="total_reward_x_claimed")
    total_reward_y_claimed: str = Field(default=..., alias="total_reward_y_claimed")
