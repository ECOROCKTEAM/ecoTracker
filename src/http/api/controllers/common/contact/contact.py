from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.dto.m2m.user.contact import ContactUserUpdateDTO
from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.contact.contact_get_favorite import ContactUserGetFavoriteUsecase
from src.core.usecases.contact.contact_set_favorite import ContactUserSetFavoriteUsecase
from src.core.usecases.contact.contact_user_create import ContactUserCreateUsecase
from src.core.usecases.contact.contact_user_get import ContactUserGetUsecase
from src.core.usecases.contact.contact_user_list import ContactUserListUsecase
from src.core.usecases.contact.contact_user_update import ContactUserUpdateUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.contact import (
    ContactCreateSchema,
    ContactFilterSchema,
    ContactListSchema,
    ContactSchema,
)
from src.http.api.schemas.utils import SortSchema

router = APIRouter()


@router.get("/list")
async def contact_lst(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    sorting: SortSchema = Depends(),
    fltr: ContactFilterSchema = Depends(),
) -> ContactListSchema:
    filter_obj = fltr.to_obj()
    sorting_obj = sorting.to_obj()

    uc = ContactUserListUsecase(uow=uow)
    result = await uc(user=user, filter_obj=filter_obj, sorting_obj=sorting_obj)
    return ContactListSchema.from_obj(contact_list=result.items)


@router.get("/{id}")
async def contact_get(
    id: int, user: Annotated[User, Depends(get_user_stub)], uow: Annotated[IUnitOfWork, Depends(get_uow_stub)]
) -> ContactSchema:
    uc = ContactUserGetUsecase(uow=uow)
    result = await uc(user=user, id=id)
    return ContactSchema.from_obj(contact=result.item)


@router.post("/")
async def contact_create(
    in_obj: ContactCreateSchema,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> ContactSchema:
    obj = in_obj.to_obj()
    uc = ContactUserCreateUsecase(uow=uow)
    result = await uc(user=user, obj=obj)
    return ContactSchema.from_obj(contact=result.item)


@router.patch("/{id}")
async def contact_update(
    id: int,
    obj: ContactUserUpdateDTO,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> ContactSchema:
    uc = ContactUserUpdateUsecase(uow=uow)
    result = await uc(id=id, user=user, obj=obj)
    return ContactSchema.from_obj(contact=result.item)


@router.patch("/{id}/favorite/")
async def contact_set_favorite(
    id: int,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> ContactSchema:
    uc = ContactUserSetFavoriteUsecase(uow=uow)
    result = await uc(user=user, id=id)
    return ContactSchema.from_obj(contact=result.item)


@router.get("/favorite/")
async def contact_get_favorite(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> ContactSchema:
    uc = ContactUserGetFavoriteUsecase(uow=uow)
    result = await uc(user=user)
    return ContactSchema.from_obj(contact=result.item)
