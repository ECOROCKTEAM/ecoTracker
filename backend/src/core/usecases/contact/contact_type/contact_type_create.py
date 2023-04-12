from dataclasses import dataclass
from typing import Union

from src.core.exeption.base import RepoError
from src.core.dto.contact import ContactTypeCreateDTO
from src.core.entity.contact import ContactType
from src.core.interfaces.base import BaseAbstractRepo


@dataclass
class SuccessResult:
    item: ContactType


@dataclass
class FailOperation:
    message: str


class ContactTypeCreateUC:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, name: str) -> Union[SuccessResult, FailOperation]:

        contact_type = ContactTypeCreateDTO(name=name)

        try:
            new_contact_type = self.repo.contact_type_create(contact_type=contact_type)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(item=new_contact_type)
