from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.task import Task
from src.core.exception.base import RepoError


@dataclass
class SuccessResult:
    item: Task


@dataclass
class FailOperation:
    message: str


class UseCase:
    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, name: str) -> Union[SuccessResult, FailOperation]:
        try:
            task = self.repo.task_get(name=name)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(item=task)
