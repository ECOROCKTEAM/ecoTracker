from dataclasses import dataclass

from src.core.dto.m2m.user.subscription import (
    UserSubscription,
    UserSubscriptionCreateDTO,
    UserSubscriptionUpdateDTO,
)
from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork


@dataclass
class Result:
    item: UserSubscription


class UserSubscriptionUpdateUsecase:
    def __init__(
        self,
        uow: IUnitOfWork,
    ) -> None:
        self.uow = uow

    async def __call__(self, user: User, obj: UserSubscriptionUpdateDTO) -> Result:
        if user.is_premium and user.subscription.id == obj.subscription_id:
            """If user wants to extend date of paid subscription."""

            old_user_sub = await self.uow.user_subscription.get(user_id=user.id, sub_id=user.subscription.id)
            old_until_date = old_user_sub.until_date
            obj.until_date += old_until_date

            await self.uow.user_subscription.delete(user_id=user.id, sub_id=user.subscription.id)

            new_obj = UserSubscriptionCreateDTO(
                user_id=user.id,
                subscription_id=obj.subscription_id,
                until_date=obj.until_date,
            )

            new_user_paid_sub = await self.uow.user_subscription.create(obj=new_obj)
            return Result(item=new_user_paid_sub)

        if user.is_premium and obj.subscription_id != user.subscription.id:
            """If the user subscription has ended."""

            id_user_paid_sub = user.subscription.id
            await self.uow.user.update_subscription(user_id=user.id, sub_id=obj.subscription_id)
            await self.uow.user_subscription.delete(user_id=user.id, sub_id=id_user_paid_sub)

            user_sub = await self.uow.user_subscription.get(user_id=user.id, sub_id=user.subscription.id)

            return Result(item=user_sub)

        if not user.is_premium:
            """If user bought premium subscription"""

            obj = UserSubscriptionCreateDTO(
                user_id=user.id,
                subscription_id=obj.subscription_id,
                until_date=obj.until_date,
            )  # type: ignore

            new_paid_sub = await self.uow.user_subscription.create(obj=obj)  # type: ignore
            await self.uow.user.update_subscription(user_id=user.id, sub_id=obj.subscription_id)
            return Result(item=new_paid_sub)

        await self.uow.subscription.list(filter_obj=MockObj)[0]  # type: ignore

        sub = await self.uow.user_subscription.update(obj=obj)
        return Result(item=sub)
