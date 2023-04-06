from enum import Enum


class RelatedEnum(str, Enum):
    USER = "USER"
    COMMUNITY = "COMMUNITY"


class VariableTypeEnum(Enum):
    STR = str
    INT = int
    BOOL = bool
