from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    result: bool


@dataclass
class FailOperation:
    message: str


class MissionCommunityDeleteUC:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, *, name: str) -> Union[SuccessResult, FailOperation]:

        try:
            _ = self.repo.mission_community_delete(name=name)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(result=True)
