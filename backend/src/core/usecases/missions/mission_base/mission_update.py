from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exception.base import RepoError


@dataclass
class SuccessResult:
    item: MissionBase


@dataclass
class FailOperation:
    message: str


class MissionBaseUpdateUC:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, status_name: str, mission_name: str) -> Union[SuccessResult, FailOperation]:
                            
        
        try:
            change = self.repo.mission_base_update(status_name=status_name, mission_name=mission_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=change)
    