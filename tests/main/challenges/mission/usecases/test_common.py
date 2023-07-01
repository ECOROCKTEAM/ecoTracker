import pytest

from src.core.dto.mock import MockObj
from src.core.entity.user import User
from src.core.exception.user import UserIsNotPremiumError
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.challenges.mission import (
    mission_community_create,
    mission_community_get,
    mission_community_list,
    mission_community_update,
    mission_get,
    mission_list,
    mission_user_create,
    mission_user_get,
    mission_user_list,
    mission_user_update,
)
from tests.fixtures.user.usecase.entity import fxe_user_default, fxe_user_not_premium


# pytest tests/main/challenges/mission/usecases/test_common.py::test_access_only_premium -v -s
@pytest.mark.asyncio
async def test_access_only_premium(
    uow: IUnitOfWork,
    fxe_user_default: User,
    fxe_user_not_premium: User,
):
    default_kw_lst = dict(
        order_obj=MockObj(),
        pagination_obj=MockObj(),
    )
    user_kw = dict(user=fxe_user_default)
    usecase_map = (
        (mission_get.MissionGetUsecase, dict(**user_kw, id=1)),
        (mission_list.MissionListUsecase, dict(**user_kw, **default_kw_lst, filter_obj="")),
        (mission_community_list.MissionCommunityListUsecase, dict(**user_kw, **default_kw_lst, filter_obj="")),
        (mission_community_get.MissionCommunityGetUsecase, dict(**user_kw, id=1, community_id=1)),
        (mission_community_create.MissionCommunityCreateUsecase, dict(**user_kw, community_id=1, create_obj="")),
        (mission_community_update.MissionCommunityUpdateUsecase, dict(**user_kw, id=1, community_id=1, update_obj="")),
        (mission_user_create.MissionUserCreateUsecase, dict(**user_kw, create_obj="")),
        (mission_user_get.MissionUserGetUsecase, dict(**user_kw, id=1)),
        (mission_user_list.MissionUserListUsecase, dict(**user_kw, **default_kw_lst, filter_obj="")),
        (mission_user_update.MissionUserUpdateUsecase, dict(**user_kw, id=1, update_obj="")),
    )
    for usecase_cls, init_data in usecase_map:
        usecase = usecase_cls(uow=uow)
        try:
            _ = await usecase(**init_data)  # type: ignore
        except UserIsNotPremiumError as e:
            raise RuntimeError("Test failure") from e
        except Exception:
            pass

    user_kw = dict(user=fxe_user_not_premium)
    usecase_map = (
        (mission_get.MissionGetUsecase, dict(**user_kw, id=1)),
        (mission_list.MissionListUsecase, dict(**user_kw, **default_kw_lst, filter_obj="")),
        (mission_community_list.MissionCommunityListUsecase, dict(**user_kw, **default_kw_lst, filter_obj="")),
        (mission_community_get.MissionCommunityGetUsecase, dict(**user_kw, id=1, community_id=1)),
        (mission_community_create.MissionCommunityCreateUsecase, dict(**user_kw, community_id=1, create_obj="")),
        (mission_community_update.MissionCommunityUpdateUsecase, dict(**user_kw, id=1, community_id=1, update_obj="")),
        (mission_user_create.MissionUserCreateUsecase, dict(**user_kw, create_obj="")),
        (mission_user_get.MissionUserGetUsecase, dict(**user_kw, id=1)),
        (mission_user_list.MissionUserListUsecase, dict(**user_kw, **default_kw_lst, filter_obj="")),
        (mission_user_update.MissionUserUpdateUsecase, dict(**user_kw, id=1, update_obj="")),
    )
    for usecase_cls, init_data in usecase_map:
        usecase = usecase_cls(uow=uow)
        with pytest.raises(UserIsNotPremiumError):
            _ = await usecase(**init_data)  # type: ignore
