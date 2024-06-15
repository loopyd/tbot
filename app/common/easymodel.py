import json
from typing import Iterable, Optional, Type, TypeVar
from pydantic import BaseModel, ConfigDict

class EasyModel(BaseModel):
    """
    A BaseModel subclass that provides easy serialization and deserialization methods.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        pass
    
    def to_dict(self, include: Optional[Iterable[str]] = None, exclude: Optional[Iterable[str]] = None) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True, include=include, exclude=exclude)

    def to_json(self, include: Optional[Iterable[str]] = None, exclude: Optional[Iterable[str]] = None) -> str:
        return json.dumps(self.to_dict(include=include,
                   exclude=exclude), ensure_ascii=True)

    @classmethod
    def from_dict(cls, data: dict, include: Optional[Iterable[str]] = None, exclude: Optional[Iterable[str]] = None) -> 'EasyModel':
        """
        Create a new isntance of the object from a dictionary.
        """
        processed = {k: v for k, v in data.items() if (
            not include or k in include) and (not exclude or k not in exclude)}
        return cls(**processed)

    @classmethod
    def from_json(cls, json_str: str, include: Optional[Iterable[str]] = None, exclude: Optional[Iterable[str]] = None) -> 'EasyModel':
        return cls.from_dict(json.loads(json_str), include=include, exclude=exclude)
