from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exception.base import RepoError


@dataclass
class Result:
    item: MissionBase


@dataclass
class FailOperation:
    message: str


class MissionBaseGetUC:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, mission_name: str) -> Union[Result, FailOperation]:

        try:
            mission = self.repo.mission_base_get(mission_name=mission_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return Result(item=mission)
    