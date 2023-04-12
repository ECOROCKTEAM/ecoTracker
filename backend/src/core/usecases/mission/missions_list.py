from dataclasses import dataclass, field
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    items: list[MissionBase] = field(default_factory=list)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self) -> Union[SuccessResult, FailOperation]:
                            
        
        try:
            missions = self.repo.missions_list()
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=missions)
    