from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.group.group_create import GroupCreateUsecase
from src.core.usecases.group.group_delete import GroupDeleteUsecase
from src.core.usecases.group.group_get import GroupGetUsecase
from src.core.usecases.group.group_list import GroupListUsecase
from src.core.usecases.group.group_update import GroupUpdateUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.group.group import (
    GroupCreateSchema,
    GroupDeleteSchema,
    GroupListFilterSchema,
    GroupListSchema,
    GroupListSortingSchema,
    GroupSchema,
    GroupUpdateSchema,
)
from src.http.api.schemas.utils import IterableSchema

router = APIRouter()


@router.get("/list")
async def group_list(
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    fltr: GroupListFilterSchema = Depends(),
    sorting: GroupListSortingSchema = Depends(),
    iterable: IterableSchema = Depends(),
) -> GroupListSchema:
    filter_obj = fltr.to_obj()
    sorting_obj = sorting.to_obj()
    iterable_obj = iterable.to_obj()
    uc = GroupListUsecase(uow=uow)
    res = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj, iterable_obj=iterable_obj)
    return GroupListSchema.from_obj(group_list=res.item, limit=res.limit, offset=res.offset, total=res.total)


@router.get("/{id}")
async def group_get(
    id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> GroupSchema:
    uc = GroupGetUsecase(uow=uow)
    res = await uc(user=user, group_id=id)
    return GroupSchema.from_obj(group=res.item)


@router.delete("/")
async def group_delete(
    id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> GroupDeleteSchema:
    uc = GroupDeleteUsecase(uow=uow)
    res = await uc(user=user, group_id=id)
    return GroupDeleteSchema(group_id=res.item)


@router.post("/")
async def group_create(
    in_obj: GroupCreateSchema,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
) -> GroupSchema:
    obj = in_obj.to_obj()

    uc = GroupCreateUsecase(uow=uow)
    res = await uc(user=user, create_obj=obj)
    return GroupSchema.from_obj(group=res.item)


@router.patch("/")
async def group_update(
    id: int,
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    user: Annotated[User, Depends(get_user_stub)],
    in_obj: GroupUpdateSchema = Depends(),
) -> GroupSchema:
    update_obj = in_obj.to_obj()
    uc = GroupUpdateUsecase(uow=uow)
    res = await uc(user=user, group_id=id, update_obj=update_obj)
    return GroupSchema.from_obj(group=res.item)
