from dataclasses import dataclass, field
from typing import Union, List

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.task import Task
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    items: list[Task] = field(default_factory=list)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo
        

    def realization(self) -> Union[SuccessResult, FailOperation]:
        
        try:
            list_of_tasks = self.repo.tasks_list()
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=list_of_tasks)