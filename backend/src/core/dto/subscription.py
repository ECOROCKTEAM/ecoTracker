from typing import List
from dataclasses import dataclass

from backend.src.core.dto.base import TypeDTO
from backend.src.core.enum.base import VariableTypeEnum
from backend.src.core.mixin.base import VariableTypeCastMixin, VariableValueType


@dataclass
class SubscriptionPeriodTypeDTO(TypeDTO):
    name: str


@dataclass
class SubscriptionPeriodDTO:
    name: str
    value: int
    type: SubscriptionPeriodTypeDTO


@dataclass
class SubscriptionConstrainsDTO(VariableTypeCastMixin):
    name: str
    _raw_value: str
    type: VariableTypeEnum

    @property
    def value(self) -> VariableValueType:
        return self._cast_type(value=self._raw_value, to_type=self.type)


@dataclass
class SubscriptionListConstrainsDTO:
    name: str
    constrains: List[SubscriptionConstrainsDTO]


@dataclass
class SubscriptionTypeDTO:
    name: str
