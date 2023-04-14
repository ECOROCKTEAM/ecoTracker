# from dataclasses import dataclass
# from typing import Union

# from src.core.interfaces.base import BaseAbstractRepo
# from src.core.exception.base import RepoError


# @dataclass
# class Result:
#     result: bool


# @dataclass
# class FailOperation:
#     message: str


# class UseCase:

#     def __init__(self, repo: BaseAbstractRepo) -> None:
#         self.repo = repo


#     def realization(self, name: str) -> Union[Result, FailOperation]:
        
#         try:
#             _ = self.repo.task_delete(name=name)
#         except RepoError as e:
#             return FailOperation(message=e)
        
#         return Result(result=True)