from datetime import datetime
from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionCommunity
from src.core.exception.base import RepoError
from src.core.dto.mission import CreateMissionCommunityDTO


@dataclass
class SuccessResult:
    item: MissionCommunity


@dataclass
class FailOperation:
    message: str


class MissionCommunityCreateUC:
    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(
        self,
        *,
        username: str,
        meeting_date: datetime,
        people_required: int,
        people_max: int,
        place: str,
        comment: str,
    ) -> Union[SuccessResult, FailOperation]:
        mission = CreateMissionCommunityDTO(
            author=username,
            meeting_date=meeting_date,
            people_required=people_required,
            people_max=people_max,
            place=place,
            comment=comment,
        )

        try:
            new_mission = self.repo.mission_comminuty_create(new_mission=mission)
        except RepoError as e:
            return FailOperation(message=e)

        return SuccessResult(item=new_mission)
