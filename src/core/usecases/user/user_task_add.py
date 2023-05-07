from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.entity.user import User
from src.core.interfaces.repository.user.task import IUserTaskRepository
from src.core.dto.m2m.user.task import UserTaskCreateDTO, UserTaskDTO
from src.core.exception.user import UserIsNotActivateError, UserTaskMaxAmountError


@dataclass
class Result:
    item: UserTaskDTO


# Fix after rebuild tasks architecture


class UserTaskAddUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        tasks = await self.repo.list(user_id=user.id)

        if len(tasks) == 3:
            raise UserTaskMaxAmountError(user_id=user.id)

        obj = UserTaskCreateDTO(
            user_id=user.id,
            task_id=task_id,
            occupancy=OccupancyStatusEnum.ACTIVE,
        )

        add = await self.repo.create(obj=obj)

        return Result(item=add)
