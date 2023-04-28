from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import UserTask


@dataclass
class Result:
    item: bool


"""
не забыть потом сделать проверку: 1 задание в день
"""


class UserTaskDoneUseCase:
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_task: UserTask) -> Result:
        add = await self.repo.user_task_done(obj=user_task)

        return Result(item=add)
