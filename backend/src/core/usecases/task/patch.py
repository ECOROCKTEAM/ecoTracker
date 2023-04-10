from dataclasses import dataclass
from typing import Union

from src.core.dto.tasks import CreateTaskDTO
from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.task import Task
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: Task


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
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
            pathed_task = self.repo.patch_task(updated_task=task)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=pathed_task)

