##############################################################
# Everything in this file will be moved to admin application #
##############################################################

# from dataclasses import dataclass

# from src.core.interfaces.repository.challenges.task import IRepositoryTask
# from src.core.entity.task import TaskCreateDTO
# from src.core.entity.user import User
# from src.core.entity.task import Task


# @dataclass
# class Result:
#     item: Task


# class TaskCreateUseCase:
#     def __init__(self, repo: IRepositoryTask) -> None:
#         self.repo = repo

#     async def __call__(self, *, user: User, obj: TaskCreateDTO) -> Result:
#         task = await self.repo.create(obj=obj)
#         return Result(item=task)
