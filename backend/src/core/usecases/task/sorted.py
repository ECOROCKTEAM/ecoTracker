from typing import List

from dataclasses import dataclass, field
from typing import Union

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

    def realization(self, category_name: str) -> Union[SuccessResult, FailOperation]:
         
        try:
            sorted_list = self.repo.sorted_task_by_category(category_name=category_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(items=sorted_list)
    