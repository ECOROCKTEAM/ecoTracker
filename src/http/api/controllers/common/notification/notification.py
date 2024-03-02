from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.notifications.get_notifications_count import (
    GetNotificationsCountUsecase,
)
from src.core.usecases.notifications.get_notifications_list import (
    GetNotificationsListUsecase,
)
from src.core.usecases.notifications.mark_as_viewed import (
    MarkNotificationsAsViewedUsecase,
)
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.notification import (
    NotificationCountSchema,
    NotificationFilterSchema,
    NotificationIdListSchema,
    NotificationListSchema,
)

router = APIRouter()


@router.get("/list")
async def notification_list(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
    fltr: NotificationFilterSchema = Depends(),
) -> NotificationListSchema:
    filter_obj = fltr.to_obj()

    uc = GetNotificationsListUsecase(uow=uow)
    result = await uc(user=user, filter_obj=filter_obj)
    return NotificationListSchema.from_obj(notification_list=result.item)


@router.get("/count")
async def notification_count(
    user: Annotated[User, Depends(get_user_stub)], uow: Annotated[IUnitOfWork, Depends(get_uow_stub)]
) -> NotificationCountSchema:
    uc = GetNotificationsCountUsecase(uow=uow)
    result = await uc(user=user)
    return NotificationCountSchema(count=result.item)


@router.post("/read")
async def noitification_read(
    in_obj: NotificationIdListSchema,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> NotificationIdListSchema:
    uc = MarkNotificationsAsViewedUsecase(uow=uow)
    result = await uc(user=user, ids=in_obj.ids)
    return NotificationIdListSchema(ids=result.item)
