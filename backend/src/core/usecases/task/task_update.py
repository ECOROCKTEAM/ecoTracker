from dataclasses import dataclass
from typing import Union

from src.core.dto.tasks import UpdateTaskDTO
from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.task import Task
from src.core.exeption.base import RepoError


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
        
        task = UpdateTaskDTO(
            name=name,
            description=description,
            score=score,
            category=category,
        )
        
        try:
            pathed_task = self.repo.task_update(updated_task=task)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=pathed_task)

