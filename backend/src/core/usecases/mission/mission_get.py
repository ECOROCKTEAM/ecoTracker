from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: MissionBase


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, mission_name: str) -> Union[SuccessResult, FailOperation]:

        try:
            mission = self.repo.mission_get(mission_name=mission_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=mission)
    