from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import UserTask


@dataclass
class Result:
    item: UserTask


"""
не забыть потом сделать проверку: 1 задание в день
"""


class UserTaskDoneUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user_task: UserTask) -> Result:

        #Ухожу. Доделать

        add = await self.repo.user_task_done(user_id=user_task.username, task_id=user_task.task_id)

        return Result(item=add)
