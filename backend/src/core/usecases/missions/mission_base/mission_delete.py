from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exception.base import RepoError


@dataclass
class SuccessResult:
    item: bool


@dataclass
class FailOperation:
    message: str


class MissionBaseDeleteUC:
    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, mission_name: str) -> Union[SuccessResult, FailOperation]:
        try:
            _ = self.repo.mission_base_delete(mission_name=mission_name)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(result=True)
