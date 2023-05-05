##############################################################
# Everything in this file will be moved to admin application #
##############################################################

# from dataclasses import dataclass
# from src.core.entity.user import User

# from src.core.interfaces.repository.challenges.mission import IRepositoryMission


# @dataclass
# class Result:
#     item: int


# class MissionDeleteUsecase:
#     def __init__(self, *, repo: IRepositoryMission) -> None:
#         self.repo = repo

#     async def __call__(self, *, user: User, id: int) -> Result:
#         rm_id = await self.repo.deactivate(id=id)
#         return Result(item=rm_id)
