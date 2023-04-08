from dataclasses import dataclass, field

from src.core.enum.base import RelatedEnum


@dataclass
class TypeDTO:
    name: str


@dataclass
class ScoreBaseDTO:
    value: int
    related: RelatedEnum = field(init=False)
