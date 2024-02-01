from dataclasses import dataclass

# from src.core.dto.mock import MockObj
# from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: User


class UserCreateUseCase:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, *, obj: UserCreateDTO) -> Result:
        # subscription = await self.uow.subscription.lst(filter_obj=MockObj())
        async with self.uow as uow:
            # subscription = Subscription()
            user = await self.uow.user.create(obj=obj)
            await uow.commit()
        return Result(item=user)
