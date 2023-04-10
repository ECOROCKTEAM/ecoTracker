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

    def realization(self, community_name: str) -> Union[SuccessResult, FailOperation]:
                        
        try:
            users = self.repo.list_of_community_users(community_name=community_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=users)
    