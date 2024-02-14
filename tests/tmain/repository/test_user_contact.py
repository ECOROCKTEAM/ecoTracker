from dataclasses import asdict

import pytest

from src.core.dto.m2m.user.contact import ContactUserCreateDTO, ContactUserUpdateDTO
from src.core.enum.user.contact import ContactTypeEnum
from src.core.exception.base import EntityNotChange, EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.user.contact import (
    IUserContactRepository,
    UserContactFilter,
    UserContactOrder,
    UserContactSorting,
)
from tests.dataloader import dataloader


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_get_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data, asrt_result",
    [
        (
            ContactUserCreateDTO(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
            dict(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
        ),
        (
            ContactUserCreateDTO(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=False),
            dict(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=False),
        ),
    ],
)
async def test_user_contact_get_ok(
    dl: dataloader, user_contact_repo: IUserContactRepository, create_data: ContactUserCreateDTO, asrt_result: dict
):
    print()
    user = await dl.user_loader.create()
    user_contact_create = await dl.user_contact_loader.create(user_id=user.id, **asdict(create_data))

    user_contact = await user_contact_repo.get(id=user_contact_create.id, user_id=user.id)

    asrt_result["id"] = user_contact_create.id
    asrt_result["user_id"] = user.id

    assert asrt_result == asdict(user_contact)


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_create_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data, asrt_result",
    [
        (
            ContactUserCreateDTO(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
            dict(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
        ),
        (
            ContactUserCreateDTO(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=False),
            dict(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=False),
        ),
    ],
)
async def test_user_contact_create_ok(
    dl: dataloader, user_contact_repo: IUserContactRepository, create_data: ContactUserCreateDTO, asrt_result: dict
):
    print()
    user = await dl.user_loader.create()
    user_contact_create = await user_contact_repo.create(user_id=user.id, obj=create_data)

    asrt_result["id"] = user_contact_create.id
    asrt_result["user_id"] = user.id

    user_contact = await user_contact_repo.get(id=user_contact_create.id, user_id=user.id)

    assert asrt_result == asdict(user_contact)
    assert asrt_result == asdict(user_contact_create)


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_create_fail_index -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_obj",
    [
        ContactUserCreateDTO(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
    ],
)
async def test_user_contact_create_fail_index(
    dl: dataloader, user_contact_repo: IUserContactRepository, create_obj: ContactUserCreateDTO
):
    user = await dl.user_loader.create()
    await user_contact_repo.create(user_id=user.id, obj=create_obj)

    with pytest.raises(EntityNotCreated) as error:
        await user_contact_repo.create(
            user_id=user.id,
            obj=ContactUserCreateDTO(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=True),
        )
        await dl.commit()
    assert "Uniq failed" in str(error.value)


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_create_unique_fail -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_obj",
    [
        ContactUserCreateDTO(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
    ],
)
async def test_user_contact_create_unique_fail(
    dl: dataloader, user_contact_repo: IUserContactRepository, create_obj: ContactUserCreateDTO
):
    print()

    user = await dl.user_loader.create()
    await user_contact_repo.create(user_id=user.id, obj=create_obj)

    with pytest.raises(EntityNotCreated) as error:
        await user_contact_repo.create(user_id=user.id, obj=create_obj)
        await dl.commit()
    assert "Uniq failed" in str(error.value)


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_get_favorite_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_data, asrt_result",
    [
        (
            ContactUserCreateDTO(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
            dict(value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True),
        ),
        (
            ContactUserCreateDTO(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=True),
            dict(value="+1234567890", type=ContactTypeEnum.PHONE, active=True, is_favorite=True),
        ),
    ],
)
async def test_user_contact_get_favorite_ok(
    dl: dataloader, user_contact_repo: IUserContactRepository, create_data: ContactUserCreateDTO, asrt_result: dict
):
    print()
    user = await dl.user_loader.create()
    user_contact_create = await dl.user_contact_loader.create(user_id=user.id, **asdict(create_data))

    user_contact = await user_contact_repo.get_favorite(user_id=user.id)

    asrt_result["id"] = user_contact_create.id
    asrt_result["user_id"] = user.id

    assert user_contact.is_favorite == True
    assert asrt_result == asdict(user_contact)


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_delete_ok -v -s
@pytest.mark.asyncio
async def test_user_contact_delete_ok(dl: dataloader, user_contact_repo: IUserContactRepository):
    user = await dl.user_loader.create()
    user_contact_model = await dl.user_contact_loader.create(user_id=user.id)

    user_contact_delete = await user_contact_repo.delete(id=user_contact_model.id, user_id=user.id)

    assert isinstance(user_contact_delete, int)
    assert user_contact_delete == user_contact_model.id


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_delete_fail -v -s
@pytest.mark.asyncio
async def test_user_contact_delete_fail(dl: dataloader, user_contact_repo: IUserContactRepository):
    user = await dl.user_loader.create()

    with pytest.raises(EntityNotFound) as error:
        id = 1
        await user_contact_repo.delete(id=id, user_id=user.id)
    assert f"User contact {id=} not found" in str(error.value)

    # pytest tests/tmain/repository/test_user_contpytest tests/tmain/repository/test_user_contact.py::test_user_contact_delete_fail -v -s: dataloader, user_contact_repo: IUserContactRepository):
    user = await dl.user_loader.create()
    user_contact_model = await dl.user_contact_loader.create(user_id=user.id, is_favorite=False)

    user_contact = await user_contact_repo.set_favorite(id=user_contact_model.id, is_favorite=True)

    assert user_contact.id == user_contact_model.id
    assert user_contact.user_id == user.id
    assert user_contact.is_favorite == True


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_update_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_obj", [ContactUserUpdateDTO(id=123, value="+12345646794", type=ContactTypeEnum.PHONE, active=True)]
)
async def test_user_contact_update_ok(
    dl: dataloader, user_contact_repo: IUserContactRepository, update_obj: ContactUserUpdateDTO
):
    user = await dl.user_loader.create()
    user_contact_model = await dl.user_contact_loader.create(user_id=user.id, id=update_obj.id)

    user_contact = await user_contact_repo.update(obj=update_obj, user_id=user.id)

    assert user_contact.id == user_contact_model.id
    assert user_contact.user_id == user.id
    assert user_contact.active == update_obj.active
    assert user_contact.type == update_obj.type
    assert user_contact.value == update_obj.value


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_update_unique_fail -v -s
@pytest.mark.asyncio
async def test_user_contact_update_unique_fail(dl: dataloader, user_contact_repo: IUserContactRepository):
    user = await dl.user_loader.create()
    user_contact_model_1 = await dl.user_contact_loader.create(user_id=user.id)
    user_contact_model_2 = await dl.user_contact_loader.create(
        user_id=user.id, value="marshall", type=ContactTypeEnum.CUSTOM, is_favorite=False
    )

    update_obj = ContactUserUpdateDTO(
        id=user_contact_model_2.id, value=user_contact_model_1.value, type=user_contact_model_1.type
    )

    with pytest.raises(EntityNotChange) as error:
        await user_contact_repo.update(obj=update_obj, user_id=user.id)
    assert "Uniq failed" in str(error.value)


async def _test_user_contact_list_first_variant(dl: dataloader) -> tuple[str, UserContactFilter]:
    user = await dl.user_loader.create()
    await dl.user_contact_loader.create(user_id=user.id, is_favorite=False)
    await dl.user_contact_loader.create(user_id=user.id, value="some@gmail.com", is_favorite=False)
    await dl.user_contact_loader.create(user_id=user.id, value="qwe@gmail.com", is_favorite=False)
    filter_obj = UserContactFilter(is_favorite=False)
    return user.id, filter_obj


async def _test_user_contact_list_second_variant(dl: dataloader) -> tuple[str, UserContactFilter]:
    user = await dl.user_loader.create()
    await dl.user_contact_loader.create(user_id=user.id, is_favorite=False)
    await dl.user_contact_loader.create(user_id=user.id, value="some@gmail.com", is_favorite=False)
    await dl.user_contact_loader.create(user_id=user.id, value="qwe@gmail.com", is_favorite=False)
    filter_obj = UserContactFilter(active=True)
    return user.id, filter_obj


async def _test_user_contact_list_third_variant(dl: dataloader) -> tuple[str, UserContactFilter]:
    user = await dl.user_loader.create()
    await dl.user_contact_loader.create(user_id=user.id, is_favorite=False)
    await dl.user_contact_loader.create(user_id=user.id, value="some@gmail.com", is_favorite=False)
    await dl.user_contact_loader.create(user_id=user.id, value="qwe@gmail.com", is_favorite=False)
    filter_obj = UserContactFilter(type=ContactTypeEnum.GMAIL)
    return user.id, filter_obj


# pytest tests/tmain/repository/test_user_contact.py::test_user_contact_list_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "arrange_func",
    [
        _test_user_contact_list_first_variant,
        _test_user_contact_list_second_variant,
        _test_user_contact_list_third_variant,
    ],
)
async def test_user_contact_list_ok(dl: dataloader, user_contact_repo: IUserContactRepository, arrange_func):
    asrt_user_id, filter_obj = await arrange_func(dl=dl)
    filter_obj: UserContactFilter = filter_obj

    user_contact_list = await user_contact_repo.list(
        user_id=asrt_user_id, filter_obj=filter_obj, sorting_obj=UserContactSorting(), order_obj=UserContactOrder()
    )

    user_id_set = set(user_contact.user_id for user_contact in user_contact_list)
    active_filter_set = set(user_contact.active for user_contact in user_contact_list)
    is_favorite_set = set(user_contact.is_favorite for user_contact in user_contact_list)
    type_set = set(user_contact.type for user_contact in user_contact_list)

    assert set([asrt_user_id]) == user_id_set
    if filter_obj.type is not None:
        assert filter_obj.type in type_set
    if filter_obj.active is not None:
        assert filter_obj.active in active_filter_set
    if filter_obj.is_favorite is not None:
        assert filter_obj.is_favorite in is_favorite_set
