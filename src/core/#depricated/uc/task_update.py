##############################################################
# Everything in this file will be moved to admin application #
##############################################################

# from dataclasses import dataclass

# from src.core.entity.task import Task, TaskUpdateDTO
# from src.core.interfaces.repository.challenges.task import IRepositoryTask
# from src.core.entity.user import User
# from src.core.exception.user import UserIsNotActivateError


# @dataclass
# class Result:
#     item: Task


# class TaskUpdateUseCase:
#     def __init__(self, repo: IRepositoryTask) -> None:
#         self.repo = repo

#     async def __call__(self, *, user: User, obj: TaskUpdateDTO) -> Result:
#         if not user.active:
#             raise UserIsNotActivateError(username=user.username)

#         task = await self.repo.update(obj=obj)
#         return Result(item=task)
