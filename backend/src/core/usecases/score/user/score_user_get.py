from dataclasses import dataclass
from typing import Union

from src.core.exception.base import RepoError
from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.score import ScoreUser


@dataclass
class Result:
    item: ScoreUser


@dataclass
class FailResult:
    messsage: str


class ScoreUserGetUC:

    def __init__(self, repo: BaseAbstractRepo):
        self.repo = repo

    def realization(self, *, username: str) -> Union[Result, FailResult]:

        try:
            score = self.repo.score_user_get(username=username)
        except RepoError as e:
            return FailResult(messsage=e)
        
        return Result(item=score)