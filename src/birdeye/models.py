from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import Field, field_validator, model_validator, root_validator, validator
import tzlocal

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


class BirdEyeResponse(EasyModel):
    data: Union[List[Any], Dict[str, Any]]
    success: bool


class SupportedNetworks(EasyModel):
    data: List[DefiNetwork] = Field(..., alias="data")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.data = [DefiNetwork(network) for network in self.data]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def __contains__(self, item):
        return item in self.data

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def insert(self, index, item):
        self.data.insert(index, item)

    def remove(self, item):
        self.data.remove(item)

    def pop(self, index):
        return self.data.pop(index)

    def clear(self):
        self.data.clear()

    def index(self, item):
        return self.data.index(item)

    def count(self, item):
        return self.data.count(item)

    def sort(self, key=None, reverse=False):
        self.data.sort(key=key, reverse=reverse)

    def reverse(self):
        self.data.reverse()


class TokenPrice(EasyModel):
    value: Optional[float] = Field(None, alias="value")
    updateUnixTime: Optional[datetime] = Field(
        None, alias="updateUnixTime", allow_mutation=True)
    updateHumanTime: Optional[str] = Field(
        None, alias="updateHumanTime", allow_mutation=True)
    liquidity: Optional[float] = Field(None, alias="liquidity")

    @model_validator(mode="before")
    def serialize_model(cls, values):
        update_unix_time = values.get("updateUnixTime")
        if isinstance(update_unix_time, int):
            time_stamp = datetime.fromtimestamp(update_unix_time, tz=tzlocal.get_localzone())
            values["updateHumanTime"] = time_stamp.strftime("%m-%d-%Y @ %H:%M:%S %p (%Z)")
            values["updateUnixTime"] = update_unix_time
        return values
