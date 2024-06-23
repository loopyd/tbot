"""
Python module for BirdEye API models.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, model_validator
import tzlocal

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


class BirdEyeResponse(EasyModel):
    """
    Model class for BirdEye API responses
    """
    data: Union[List[Any], Dict[str, Any]]
    success: bool


class SupportedNetworks(EasyModel):
    """
    Model class for supported networks by BirdEye API.
    """
    data: List[DefiNetwork] = Field(default=..., alias="data")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.data = [DefiNetwork(value=network) for network in self.data]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        return self.data[index]

    def __setitem__(self, index: int, value):
        self.data[index] = value

    def __delitem__(self, index: int):
        del self.data[index]

    def __contains__(self, item):
        return item in self.data

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def insert(self, index: int, item):
        self.data.insert(index, item)

    def remove(self, item):
        self.data.remove(item)

    def pop(self, index: int):
        return self.data.pop(index)

    def clear(self):
        self.data.clear()

    def index(self, item) -> int:
        return self.data.index(item)

    def count(self, item):
        return self.data.count(item)

    def sort(self, key=None, reverse=False):
        self.data.sort(key=key, reverse=reverse)

    def reverse(self):
        self.data.reverse()


class TokenPrice(EasyModel):
    """
    Model class for token price.
    """
    value: Optional[float] = Field(default=None, alias="value")
    updateUnixTime: Optional[datetime] = Field(
        default=None, alias="updateUnixTime")
    updateHumanTime: Optional[str] = Field(
        default=None, alias="updateHumanTime")
    liquidity: Optional[float] = Field(default=None, alias="liquidity")

    @model_validator(mode="before")
    def serialize_model(cls, values: Dict[str, Any]) -> Any:
        """
        Serialize the model.
        """
        update_unix_time: int | None = values.get("updateUnixTime")
        if isinstance(update_unix_time, int):
            time_stamp: datetime = datetime.fromtimestamp(
                update_unix_time, tz=tzlocal.get_localzone())
            values["updateHumanTime"] = time_stamp.strftime(
                "%m-%d-%Y @ %H:%M:%S %p (%Z)")
            values["updateUnixTime"] = update_unix_time
        return values
