from dataclasses import dataclass
from typing import Union

from backend.src.core.enum.base import VariableTypeEnum


VariableValueType = Union[int, str, bool]


@dataclass
class VariableTypeCastMixin:
    def __cast_to_bool(self, value: str) -> bool:
        return bool(value)

    def __cast_to_int(self, value: str) -> int:
        return int(value)

    @property
    def __cast_op(self) -> dict:
        return {
            VariableTypeEnum.STR: lambda x: x,
            VariableTypeEnum.INT: self.__cast_to_int,
            VariableTypeEnum.BOOL: self.__cast_to_bool,
        }

    def _cast_type(self, value: str, to_type: VariableTypeEnum) -> VariableValueType:
        f = self.__cast_op.get(to_type)
        if f is None:
            raise Exception("Not found caster")
        converted_value = f(value)
        if not isinstance(converted_value, to_type.value):
            raise Exception("Can't cast value")
        return converted_value
