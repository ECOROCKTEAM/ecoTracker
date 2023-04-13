from dataclasses import dataclass, field
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.community import Community
from src.core.exception.base import RepoError


@dataclass
class SuccessResult:
    items: list[Community] = field(default_factory=list)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self) -> Union[SuccessResult, FailOperation]:
                        
        try:
            communities = self.repo.communities_list()
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=communities)
    