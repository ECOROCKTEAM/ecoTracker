from dataclasses import dataclass, field
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exeption.base import RepoError
from src.core.dto.mission import CreateMissionDTO


@dataclass
class SuccessResult:
    item: MissionBase


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self,
                    username: str,
                    name: str,
                    description: str,
                    instruction: str,
                    score: int,
                    category: str, # или передавать DTO????
                    status: str,
                    related: str = field(init=False),
                    ) -> Union[SuccessResult, FailOperation]:
                            
        mission = CreateMissionDTO(
            name=name,
            description=description,
            instruction=instruction,
            score=score,
            category=category,
            status=status,
            related=related,
        )
        
        try:
            new_mission = self.repo.mission_create(new_mission=mission, username=username)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=new_mission)
    