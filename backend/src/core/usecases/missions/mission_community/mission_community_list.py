from dataclasses import dataclass, field
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.mission import MissionCommunity
from src.core.exception.base import RepoError


@dataclass
class Result:
    items: list[MissionCommunity] = field(default_factory=list)


@dataclass
class FailOperation:
    message: str


class MissionCommunityListUC:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self, *,
                    sorting_obj: str = None, 
                    paggination_obj: str = None, 
                    filter_obj: str = None,                    
                    ) -> Union[Result, FailOperation]:

        try:
            mission_list = self.repo.mission_community_list(
                sorting_obj=sorting_obj,
                paggination_obj=paggination_obj,
                filter_obj=filter_obj
            )
        except RepoError as e:
            return FailOperation(message=e)

        return Result(items=mission_list)
