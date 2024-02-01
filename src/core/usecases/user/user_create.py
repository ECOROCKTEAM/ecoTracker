from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserCreateDTO

# from src.core.dto.mock import MockObj
from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO
from src.core.enum.user.contact import ContactTypeEnum
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
            subscription = Subscription()
            user = await uow.user.create(user_obj=obj, sub_obj=subscription)

            _ = await uow.user_contact.create(
                obj=ContactUserCreateDTO(
                    user_id=user.id, value=user.username, type=ContactTypeEnum.GMAIL, is_favorite=True, active=True
                )
            )

            await uow.commit()

        return Result(item=user)
