from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User, UserTask
from src.core.exception.user import UserIsNotActivateError
from src.core.exception.task import TaskAlreadyTakenError 



@dataclass
class Result:
    item: UserTask


class UserTaskAddUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, task_id: int) -> Result:

        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        
        exist_task = self.repo.user_task_get(user_id=user.username, task_id=task_id)

        if exist_task:
            raise TaskAlreadyTakenError(username=user.username, task=task_id)
        
        #синхронный код?

        add = await self.repo.user_task_add(user_id=user.username, task_id=task_id)

        return Result(item=add)
