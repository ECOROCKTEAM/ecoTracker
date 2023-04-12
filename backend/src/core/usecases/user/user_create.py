from dataclasses import dataclass
from typing import Union

from src.core.enum.contact import ContactEnum
from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.user import User
from src.core.dto.user import CreateUserDTO
from src.core.exception.base import RepoError


@dataclass
class SuccessResult:
    item: User


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self,
                    username: str,
                    password: str,
                    contact: str,
                    contact_type: ContactEnum,
        ) -> Union[SuccessResult, FailOperation]:

        user = CreateUserDTO(username=username, password=password)
                
        try:
            new_user = self.repo.user_create(new_user=user)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=new_user)
    