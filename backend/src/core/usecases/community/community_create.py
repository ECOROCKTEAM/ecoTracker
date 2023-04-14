from dataclasses import dataclass
from typing import Union

from src.core.interfaces.base import BaseAbstractRepo
from src.core.entity.community import Community
from src.core.dto.community import CreateCommunityDTO
from src.core.exception.base import RepoError


@dataclass
class Result:
    item: Community


@dataclass
class FailOperation:
    message: str


class UseCase:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo

    def realization(self,
                    name: str,
                    description: str,
                    privacy: str
                ) -> Union[Result, FailOperation]:
                            
        community = CreateCommunityDTO(
            name=name,
            description=description,
            privacy=privacy,
        )

        try:
            new_community = self.repo.community_create(community)
        except RepoError as e:
            return FailOperation(message=e)
        
        return Result(item=new_community)
    
