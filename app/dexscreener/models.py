from enum import Enum
from pydantic import Field
from typing import Optional
import datetime as dt
from ..common.easymodel import EasyModel


class DefiNetwork(Enum):
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


class BaseToken(EasyModel):
    """
    A model for a token on a decentralized exchange.
    """
    address: str = Field(..., alias="address")
    name: str = Field(..., alias="name")
    symbol: str = Field(..., alias="symbol")


class TransactionCount(EasyModel):
    """
    A model for the number of buy and sell transactions.
    """
    buys: int = Field(..., alias="buys")
    sells: int = Field(..., alias="sells")


class PairTransactionCounts(EasyModel):
    """
    A model for the number of transactions in different time periods.
    """
    m5: TransactionCount = Field(default_factory=TransactionCount, alias="m5")
    h1: TransactionCount = Field(default_factory=TransactionCount, alias="h1")
    h6: TransactionCount = Field(default_factory=TransactionCount, alias="h6")
    h24: TransactionCount = Field(
        default_factory=TransactionCount, alias="h24")


class TimePeriodsFloat(EasyModel):
    """
    A model for the change in a value over different time periods.
    """
    m5: Optional[float] = Field(0.0, alias="m5")
    h1: Optional[float] = Field(0.0, alias="h1")
    h6: Optional[float] = Field(0.0, alias="h6")
    h24: Optional[float] = Field(0.0, alias="h24")


class VolumeChangePeriods(TimePeriodsFloat):
    """
    A model for the change in volume over different time periods.
    """
    ...


class PriceChangePeriods(TimePeriodsFloat):
    """
    A model for the change in price over different time periods.
    """
    ...


class Liquidity(EasyModel):
    """
    A model for the liquidity of a token pair.
    """
    usd: Optional[float] = Field(None, alias="usd")
    base: float = Field(..., alias="base")
    quote: float = Field(..., alias="quote")


class TokenPair(EasyModel):
    """
    A model for a token pair on a decentralized exchange.
    """
    chain_id: str = Field(..., alias="chainId")
    dex_id: str = Field(..., alias="dexId")
    url: str = Field(..., alias="url")
    pair_address: str = Field(..., alias="pairAddress")
    base_token: BaseToken = Field(default_factory=BaseToken, alias="baseToken")
    quote_token: BaseToken = Field(
        default_factory=BaseToken, alias="quoteToken")
    price_native: float = Field(..., alias="priceNative")
    price_usd: Optional[float] = Field(None, alias="priceUsd")
    transactions: PairTransactionCounts = Field(
        default_factory=PairTransactionCounts, alias="txns")
    volume: VolumeChangePeriods = Field(
        default_factory=VolumeChangePeriods, alias="volume")
    price_change: PriceChangePeriods = Field(
        default_factory=PriceChangePeriods, alias="priceChange")
    liquidity: Optional[Liquidity] = Field(None, alias="liquidity")
    fdv: Optional[float] = Field(None, alias="fdv")
    pair_created_at: Optional[dt.datetime] = Field(None, alias="pairCreatedAt")
