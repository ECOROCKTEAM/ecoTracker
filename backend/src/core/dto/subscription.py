from typing import List
from dataclasses import dataclass

from src.core.dto.base import TypeDTO
from src.core.enum.base import VariableTypeEnum
from src.core.mixin.base import VariableTypeCastMixin, VariableValueType


@dataclass
class SubscriptionPeriodTypeDTO(TypeDTO):
    """ """

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
    
    def __repr__(self) -> str:
        return f'{self.__class__}(name={self.name}, _raw_value={self._raw_value}, type={self.type}, value={self.value})'


@dataclass
class SubscriptionListConstrainsDTO:
    name: str
    constrains: List[SubscriptionConstrainsDTO]


@dataclass
class SubscriptionTypeDTO(TypeDTO):
    """ """
