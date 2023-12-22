# from dataclasses import dataclass

# from src.core.dto.subscription.period import SubscriptionPeriodDTO
# from src.core.entity.user import User
# from src.core.exception.user import UserIsNotActivateError
# from src.core.interfaces.repository.subscription.subscription import (
#     ISubscriptionRepository,
# )


# @dataclass
# class Result:
#     items: list[SubscriptionPeriodDTO]


class SubscriptionPeriodListUsecase:
    # def __init__(self, repo: ISubscriptionRepository) -> None:
    #     self.repo = repo

    # async def __call__(self, *, user: User) -> Result:
    #     if not user.active:
    #         raise UserIsNotActivateError(user_id=user.id)

    #     obj_list = await self.repo.period_list()
    #     return Result(items=obj_list)
    raise NotImplementedError
