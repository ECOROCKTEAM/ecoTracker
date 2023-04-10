from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import OneBigAbstractRepo
from src.core.entity.community import Community
from src.core.dto.community import CreateCommunityDTO
from src.core.exeption.base import RepoError


@dataclass
class SuccessResult:
    item: Community


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: OneBigAbstractRepo) -> None:
        self.repo = repo

    def realization(self,
                    name: str,
                    description: str,
                    privacy: str
                ) -> Union[SuccessResult, FailOperation]:
                            
        community = CreateCommunityDTO(
            name=name,
            description=description,
            privacy=privacy,
        )

        try:
            new_community = self.repo.create_community(community)
        except RepoError as e:
            return FailOperation(message=e)
        
        return SuccessResult(item=new_community)
    