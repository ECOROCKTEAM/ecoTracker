from dataclasses import dataclass
from typing import Union

from src.core.exeption.base import RepoError
from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.score import ScoreUser


@dataclass
class SuccessResult:
    item: ScoreUser


@dataclass
class FailResult:
    messsage: str


class ScoreUserGetUC:

    def __init__(self):
        self.repo = BaseAbstractRepo

    def realization(self, *, username: str) -> Union[SuccessResult, FailResult]:

        try:
            score = self.repo.score_user_get(username=username)
        except RepoError as e:
            return FailResult(messsage=e)
        
        return SuccessResult(item=score)