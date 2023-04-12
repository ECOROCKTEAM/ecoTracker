from dataclasses import dataclass, field
from typing import Union

from src.core.enum.base import RelatedEnum
from src.core.dto.occypancy import OccupancyCategoryDTO
from src.core.enum.occupancy import OccupancyStatusEnum
from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exception.base import RepoError
from src.core.dto.mission import CreateMissionBaseDTO


@dataclass
class SuccessResult:
    item: MissionBase


@dataclass
class FailOperation:
    message: str


class MissionBaseCreateUC:
    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(
        self,
        name: str,
        description: str,
        instruction: str,
        score: int,
        category: OccupancyCategoryDTO,  # или передавать DTO????
        status: OccupancyStatusEnum,
        related: RelatedEnum = field(init=False),
    ) -> Union[SuccessResult, FailOperation]:
        mission = CreateMissionBaseDTO(
            name=name,
            description=description,
            instruction=instruction,
            score=score,
            category=category,
            status=status,
            related=related,
        )

        try:
            new_mission = self.repo.mission_base_create(new_mission=mission)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(item=new_mission)
