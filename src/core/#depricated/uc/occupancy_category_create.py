##############################################################
# Everything in this file will be moved to admin application #
##############################################################

# from dataclasses import dataclass

# from src.core.dto.challenges.category import (
#     OccupancyCategoryCreateDTO,
#     OccupancyCategoryDTO,
# )
# from src.core.interfaces.repository.challenges.occupancy import IOccupancyRepository
# from src.core.entity.user import User


# @dataclass
# class Result:
#     item: OccupancyCategoryDTO


# class OccupancyCategoryCreateUseCase:
#     def __init__(self, repo: IOccupancyRepository) -> None:
#         self.repo = repo

#     async def __call__(self, *, user: User, obj: OccupancyCategoryCreateDTO) -> Result:
#         type = await self.repo.type_create(obj=obj)
#         return Result(item=type)
