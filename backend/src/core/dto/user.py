from typing import List

from dataclasses import dataclass
from backend.src.core.dto.base import ScoreBaseDTO, TypeDTO
from backend.src.core.enum.base import RelatedEnum


@dataclass
class UserContactTypeDTO(TypeDTO):
    """"""


@dataclass
class UserContactDTO:
    value: str
    active: bool
    type: UserContactTypeDTO


@dataclass
class UserContactListDTO:
    contacts: List[UserContactDTO]

    def __getattr__(self, request_type: str):
        tmp = None
        for contact in self.contacts:
            if contact.type.name == request_type:
                tmp = contact
                break
        else:
            raise Exception("Not found")
        return tmp


@dataclass
class ScoreUserDTO(ScoreBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.USER
