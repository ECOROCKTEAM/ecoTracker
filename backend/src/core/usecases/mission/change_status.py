from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: MissionBase


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo

    def realization(self, status_name: str, mission_name: str) -> Union[SuccessResult, FailOperation]:
                            
        
        try:
            change = self.repo.change_mission_status(status_name=status_name, mission_name=mission_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=change)
    