from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionCommunity
from src.core.exception.base import RepoError


@dataclass
class SuccessResult:
    item: MissionCommunity


@dataclass
class FailOperation:
    message: str


class MissionCommunityGetUC:
    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, *, name: str) -> Union[SuccessResult, FailOperation]:
        try:
            new_mission = self.repo.mission_community_get(name=name)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(item=new_mission)
