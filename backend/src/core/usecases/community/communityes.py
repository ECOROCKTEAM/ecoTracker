from dataclasses import dataclass, field
from typing import Union, List

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.community import Community
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    items: List[Community] = field(default_factory=True)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo

    def realization(self) -> Union[SuccessResult, FailOperation]:
                        
        try:
            communities = self.repo.get_communities()
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=communities)
    