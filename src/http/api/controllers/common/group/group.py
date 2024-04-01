# from typing import Annotated

# from fastapi import APIRouter, Depends

# from src.core.entity.user import User
# from src.core.interfaces.unit_of_work import IUnitOfWork
# from src.core.usecases.group.group_create import GroupCreateUsecase
# from src.http.api.depends.stub import get_uow_stub, get_user_stub
# from src.http.api.schemas.group import GroupCreateSchema, GroupSchema

# router = APIRouter()


# @router.post('/create')
# async def group_create(
#     in_obj: GroupCreateSchema,
#     uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
#     user: Annotated[User, Depends(get_user_stub)],
# ) -> GroupSchema:
#     obj = in_obj.to_obj()

#     uc = GroupCreateUsecase(uow=uow)
#     res = await uc(user=user, create_obj=obj)
#     return GroupSchema.from_obj(group=res.item)


# @router.get("/list")
# async def group_list(
#     uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
#     user: Annotated[User, Depends(get_user_stub)],
# )
