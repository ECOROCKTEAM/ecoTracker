# from dataclasses import dataclass

# from src.core.dto.mock import MockObj
# from src.core.entity.subscription import Subscription
# from src.core.entity.user import User
# from src.core.exception.user import UserIsNotActivateError
# from src.core.interfaces.repository.subscription.subscription import (
#     ISubscriptionRepository,
# )


# @dataclass
# class Result:
#     items: list[Subscription]


class SubscriptionListUsecase:
    # def __init__(self, repo: ISubscriptionRepository) -> None:
    #     self.repo = repo

    # async def __call__(self, *, user: User, filter_obj: MockObj | None = None) -> Result:
    #     if not user.active:
    #         raise UserNotActive(id=user.id

    #     sub_list = await self.repo.lst(filter_obj=filter_obj)
    #     return Result(items=sub_list)
    raise NotImplementedError
