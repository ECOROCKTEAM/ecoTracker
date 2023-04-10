from typing import List

from abc import ABC, abstractmethod

# Tasks imports
from src.core.dto.tasks import CreateTaskDTO
from src.core.entity.task import Task

# Mission imports
from src.core.dto.mission import CreateMissionDTO
from src.core.entity.mission import MissionBase

# Community imports
from src.core.dto.community import CreateCommunityDTO
from src.core.entity.community import Community

# User imports
from src.core.dto.user import CreateUserDTO
from src.core.entity.user import User


class OneBigAbstractRepo(ABC):

    # Tasks chapter
    @abstractmethod
    def create_task(self, new_task: CreateTaskDTO) -> Task: #usecase +
        pass

    @abstractmethod
    def get_task(self, name: str) -> Task:#usecase +
        pass

    @abstractmethod
    def list_of_tasks(self) -> List[Task]:#usecase +
        pass

    @abstractmethod
    def sorted_task_by_category(self, category_name: str) -> List[Task]:  #usecase +
        pass

    @abstractmethod
    def change_task_status(self, task_name: str) -> Task:  #usecase +
        pass

    @abstractmethod
    def patch_task(self, updated_task: CreateTaskDTO) -> Task: #usecase +
        pass

    @abstractmethod
    def delete_task(self, name: str) -> bool:  #usecase +
        pass

    # Mission chapter

    @abstractmethod
    def create_mission(self, new_mission: CreateMissionDTO, username: str) -> MissionBase: #usecase +
        pass

    @abstractmethod
    def get_one_mission(self, mission_name: str) -> MissionBase:  #usecase +
        pass

    @abstractmethod
    def get_missions(self) -> List[MissionBase]: #usecase + 
        pass

    @abstractmethod
    def change_mission_status(self, status_name:str, mission_name: str) -> MissionBase:  #usecase +
        pass

    @abstractmethod
    def sorted_missions_by_category(self, category_name: str) -> List[MissionBase]: #usecase +
        pass

    # Community chapter
    @abstractmethod
    def create_community(self, new_community: CreateCommunityDTO) -> Community:
        pass

    @abstractmethod
    def deactivate_community(self, community_name: str) -> bool:
        pass

    @abstractmethod
    def get_one_community(self, community_name: str) -> Community:
        pass

    @abstractmethod
    def get_communities(self) -> List[Community]:
        pass

    # User chapter

    @abstractmethod
    def create_user(self, new_user: CreateUserDTO) -> User:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> bool:
        pass

    @abstractmethod
    def get_one_user(self, username: str) -> User:
        pass

    @abstractmethod
    def list_of_community_users(self, community_name: str) -> List[User]:
        pass

    @abstractmethod
    def get_premiun_users(self, subscription_name: str) -> List[User]:
        pass

