from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.community import Community
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: Community


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, community_name: str) -> Union[SuccessResult, FailOperation]:
                        
        try:
            change = self.repo.change_community_status(community_name=community_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=change)
    