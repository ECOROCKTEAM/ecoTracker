from dataclasses import dataclass, field
from typing import Union, List

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.mission import MissionBase
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: List[MissionBase] = field(default_factory=List)


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo


    def realization(self, category_name: str) -> Union[SuccessResult, FailOperation]:
                    
        try:
            missions = self.repo.sorted_missions_by_category(category_name=category_name)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=missions)
    