from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.entity.user import User
from src.core.interfaces.user.task import IUserTaskRepository
from src.core.dto.m2m.user.task import UserTaskCreateDTO, UserTaskDTO
from src.core.exception.user import UserIsNotActivateError, UserTaskMaxAmountError


@dataclass
class Result:
    item: UserTaskDTO


class UserTaskAddUseCase:
    def __init__(self, repo: IUserTaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, task_id: int) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        
        tasks: list[UserTaskDTO] = await self.repo.list(user_id=user.username)

        if len(tasks) == 3:
            raise UserTaskMaxAmountError(username=user.username)
        
        obj = UserTaskCreateDTO(
            username=user.username,
            task_id=task_id,
            occupancy=OccupancyStatusEnum.ACTIVE 
        )
        # Хардкод? И можно ли так в принципе делать? Я хочу присваивать статус "активный" взятого задания пользователем по дефолту.
        # Хотел просто, чтобы когда пользователь брал задачу она сразу была активна. Ну это и так понятно. Хз как правильно сделать

        

        add = await self.repo.create(obj=obj)

        return Result(item=add)
