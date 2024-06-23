"""
This module provides a BaseModel subclass that provides easy serialization and deserialization methods.
"""
import json
from typing import Any, Iterable, Optional, Dict, cast
from pydantic import BaseModel, ConfigDict


class EasyModel(BaseModel):
    """
    A BaseModel subclass that provides easy serialization and deserialization methods.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_dict(
        self,
        include: Optional[Iterable[str]] = None,
        exclude: Optional[Iterable[str]] = None
    ) -> Dict[str, Any]:
        """
        Convert the object to a dictionary
        """
        include_set: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = cast(
            set[int] | set[str] | dict[int, Any] | dict[str, Any] | None, set(include)) if include is not None else None
        exclude_set: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = cast(
            set[int] | set[str] | dict[int, Any] | dict[str, Any] | None, set(exclude)) if exclude is not None else None
        return self.model_dump(
            by_alias=True,
            exclude_none=True,
            include=include_set,
            exclude=exclude_set
        )

    def to_json(
        self,
        include: Optional[Iterable[str]] = None,
        exclude: Optional[Iterable[str]] = None
    ) -> str:
        """
        Convert the object to a JSON string.
        """
        return json.dumps(self.to_dict(include=include, exclude=exclude), ensure_ascii=True)

    @classmethod
    def from_dict(
        cls,
        data: Dict[Any, Any],
        include: Optional[Iterable[str]] = None,
        exclude: Optional[Iterable[str]] = None
    ) -> "EasyModel":
        """
        Create a new isntance of the object from a dictionary.
        """
        processed: Dict[Any, Any] = {
            k: v for k, v in data.items() if (not include or k in include) and (not exclude or k not in exclude)
        }
        return cls(**processed)

    @classmethod
    def from_json(
        cls,
        json_str: str,
        include: Optional[Iterable[str]] = None,
        exclude: Optional[Iterable[str]] = None
    ) -> "EasyModel":
        """
        Create a new instance of the object from a JSON string.
        """
        return cls.from_dict(json.loads(json_str), include=include, exclude=exclude)
