from dataclasses import dataclass

from src.core.dto.application_role import ApplicationRoleDTO, UserApplicationRoleDTO, UserApplicationRoleUpdateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.exception.user import UserPermissionError, UserIsNotActivateError
from src.core.entity.user import User


@dataclass
class Result:
    item: UserApplicationRoleDTO


'''
Вероятно, мы хотим не просто сами себе обновлять роль, а предоставлять её, то есть давать от себя кому-то, поэтому
нужно получить типо себя и юзера, которому хотим назначить другую роль
''' 

class TaskCreateUseCase:

    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, updating_user: User, admin_user: User, obj: ApplicationRoleDTO) -> Result:
        
        if not admin_user.application_role.ADMIN:
            raise UserPermissionError(username=admin_user.username)            
        
        if not admin_user.active:
            raise UserIsNotActivateError(username=admin_user.username)
        if not updating_user:
            raise UserIsNotActivateError(username=updating_user.username) #Может есть возможность объеденить?...

        user = UserApplicationRoleUpdateDTO(
            username=updating_user.username,
            application_role=obj.name
        )

        app_role = await self.repo.user_role_application_update(obj=user)

        return Result(item=app_role)
        