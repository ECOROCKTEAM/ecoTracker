# from dataclasses import dataclass

# from src.core.entity.user import User, UserUpdateDTO
# from src.core.interfaces.unit_of_work import IUnitOfWork


# @dataclass
# class Result:
#     item: User


class UserUpdateUsecase:
    raise NotImplementedError
    # def __init__(self, uow: IUnitOfWork) -> None:
    #     self.uow = uow

    # async def __call__(self, *, obj: UserUpdateDTO) -> Result:
    #     user = await self.uow.user.update(obj=obj)
    #     return Result(item=user)
