from dataclasses import dataclass, field
from typing import Union, List

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.user import User
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    items: List[User] = field(default_factory=List)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo

    def realization(self, subscription_name: str) -> Union[SuccessResult, FailOperation]:
                        
        try:
            users = self.repo.get_premiun_users(subscription_name=subscription_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=users)
    