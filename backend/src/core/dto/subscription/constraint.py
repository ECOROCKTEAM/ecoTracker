from dataclasses import dataclass

from src.core.enum.variable_type import VariableTypeEnum
from src.core.mixin.variable_type import VariableTypeCastMixin
from src.core.typing.base import VariableValueType


@dataclass
class SubscriptionConstraintDTO(VariableTypeCastMixin):
    name: str
    _raw_value: str
    type: VariableTypeEnum

    @property
    def value(self) -> VariableValueType:
        return self._cast_type(value=self._raw_value, to_type=self.type)

    def __repr__(self) -> str:
        return f"{self.__class__}(name={self.name}, _raw_value={self._raw_value}, type={self.type}, value={self.value})"
