from dataclasses import dataclass, field
from typing import Union, List

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.task import Task
from src.core.exeption.base import RepoError

# Я хз правильно ли, но если нам наш репозит вернёт пустой список, то в таком случае без default_fac будет ошибка по идее
@dataclass
class SuccessResult:
    items: List[Task] = field(default_factory=List)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo
        

    def realization(self) -> Union[SuccessResult, FailOperation]:
        
        try:
            list_of_tasks = self.repo.list_of_tasks()
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=list_of_tasks)