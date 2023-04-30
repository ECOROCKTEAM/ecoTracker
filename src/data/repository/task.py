from sqlalchemy import update, delete, select
from dataclasses import asdict
from src.core.dto.m2m.user.filters import UserTaskFilter
from src.core.dto.m2m.user.task import UserTaskCreateDTO, UserTaskDTO, UserTaskUpdateDTO
from src.core.interfaces.repository.user.task import IUserTaskRepository
from src.data.models.challenges.task import TaskModel


def model_to_dto(model: TaskModel) -> UserTaskDTO:
    pass


def dto_to_model() -> TaskModel:
    pass


class UserTaskRepository(IUserTaskRepository):
    def __init__(self, db_context) -> None:
        self.db_contex = db_context

    async def update(self, *, obj: UserTaskUpdateDTO) -> UserTaskDTO:
        values = asdict(obj)
        id_ = values.pop("id")
        stmt = update(TaskModel).where(id=id_).values(**values).returning(TaskModel)
        result: TaskModel = await self.db_contex.scalars(stmt).first()
        return model_to_dto(result)

    async def delete(self, *, id: int) -> int:
        stmt = delete(TaskModel).where(TaskModel.id == id)
        result = await self.db_contex.scalars(stmt).first()
        return result

    async def get(self, *, id: int) -> UserTaskDTO:
        stmt = select(TaskModel).where(TaskModel.id == id)
        result = await self.db_contex.scalars(stmt).first()
        return model_to_dto(result)

    async def list(self, *, user_id: str, filter_obj: UserTaskFilter | None = None) -> list[UserTaskDTO]:
        pass

    async def create(self, *, obj: UserTaskCreateDTO) -> UserTaskDTO:
        pass
