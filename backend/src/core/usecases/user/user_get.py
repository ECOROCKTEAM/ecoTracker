# from dataclasses import dataclass
# from typing import Union

# from src.core.interfaces.base import BaseAbstractRepo
# from src.core.entity.user import User
# from src.core.exception.base import RepoError


# @dataclass
# class Result:
#     item: User


# @dataclass
# class FailOperation:
#     message: str


# class UseCase:

#     def __init__(self, repo: BaseAbstractRepo) -> None:
#         self.repo = repo

#     def realization(self, username: str) -> Union[Result, FailOperation]:
                        
#         try:
#             user = self.repo.user_get(username=username)
#         except RepoError as e:
#             return FailOperation(message=e)
        
#         return Result(item=user)
    