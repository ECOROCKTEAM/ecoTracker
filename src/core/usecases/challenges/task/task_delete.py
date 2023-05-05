from dataclasses import dataclass

from src.core.interfaces.repository.challenges.task import ITaskRepository
from src.core.entity.user import User


@dataclass
class Result:
    item: int


class TaskDeleteUseCase:
    def __init__(self, repo: ITaskRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, id: int) -> Result:
        rm_id = await self.repo.delete(id=id)
        return Result(item=rm_id)
