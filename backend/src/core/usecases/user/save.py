from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.user import User
from src.core.dto.user import CreateUserDTO
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: User


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo

    def realization(self,
                    username: str,
                    password: str,
        ) -> Union[SuccessResult, FailOperation]:

        user = CreateUserDTO(username=username, password=password)
                
        try:
            new_user = self.repo.create_user(new_user=user)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=new_user)
    