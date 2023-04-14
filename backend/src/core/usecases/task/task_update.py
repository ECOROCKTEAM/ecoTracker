# from dataclasses import dataclass
# from typing import Union

# from src.core.dto.tasks import UpdateTaskDTO
# from src.core.interfaces.base import BaseAbstractRepo
# from src.core.entity.task import Task
# from src.core.exception.base import RepoError


# @dataclass
# class Result:
#     item: Task


# @dataclass
# class FailOperation:
#     message: str


# class UseCase:

#     def __init__(self, repo: BaseAbstractRepo) -> None:
#         self.repo = repo

#     def realization(self,
#                     name: str,
#                     description: str,
#                     score: int,
#                     category: str,
#                     ) -> Union[Result, FailOperation]:
        
#         task = UpdateTaskDTO(
#             name=name,
#             description=description,
#             score=score,
#             category=category,
#         )
        
#         try:
#             pathed_task = self.repo.task_update(updated_task=task)
#         except RepoError as e:
#             return FailOperation(message=e)
        
#         return Result(item=pathed_task)

