from typing import Union
from dataclasses import dataclass

from src.core.dto.tasks import CreateTaskDTO
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


    def realization(self, 
                    name: str,
                    description: str,
                    score: int,
                    category: str,
                ) -> Union[SuccessResult, FailOperation]:
        
        task = CreateTaskDTO(
            name=name,
            description=description,
            score=score,
            category=category,
        )
        
        try:
            new_task = self.repo.task_create(new_task=task)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=new_task)
        