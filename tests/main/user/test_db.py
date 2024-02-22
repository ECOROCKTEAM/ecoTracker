import pytest
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.enum.user.contact import ContactTypeEnum
from src.core.exception.base import EntityNotFound
from src.data.models.user.user import UserContactModel, UserModel
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE


# pytest tests/main/user/db/test_db.py::test_user_create_with_contact -v -s
@pytest.mark.asyncio
async def test_user_create_with_contact(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(user)
    await session.commit()
    user_contact = UserContactModel(
        user_id=user.id, value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True
    )
    session.add(user_contact)
    await session.commit()

    await session.delete(user_contact)
    await session.commit()

    await session.delete(user)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_user_contact_set_favorite -v -s
@pytest.mark.asyncio
async def test_user_contact_set_favorite(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)

    session.add(user)
    await session.flush()
    user_contact_1 = UserContactModel(
        user_id=user.id, value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True
    )
    user_contact_2 = UserContactModel(
        user_id=user.id, value="+88005553535", type=ContactTypeEnum.PHONE, active=True, is_favorite=False
    )

    session.add_all([user_contact_1, user_contact_2])
    await session.commit()

    stmt_1 = (
        update(UserContactModel)
        .where(UserContactModel.id == user_contact_1.id)
        .values(is_favorite=False)
        .returning(UserContactModel)
    )
    set_favorite_as_unfavorite = await session.scalar(statement=stmt_1)
    if not set_favorite_as_unfavorite:
        raise EntityNotFound(msg="")
    stmt_2 = (
        update(UserContactModel)
        .where(UserContactModel.id == user_contact_2.id)
        .values(is_favorite=True)
        .returning(UserContactModel)
    )
    set_unfavorite_as_favorite = await session.scalar(statement=stmt_2)
    if not set_unfavorite_as_favorite:
        raise EntityNotFound(msg="")
    session.add_all([set_favorite_as_unfavorite, set_unfavorite_as_favorite])
    await session.commit()

    await session.delete(user_contact_1)
    await session.delete(user_contact_2)
    await session.commit()

    await session.delete(user)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_user_contacts_ok -v -s
@pytest.mark.asyncio
async def test_user_contacts_ok(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(user)
    await session.flush()

    user_contact_1 = UserContactModel(
        user_id=user.id, value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True
    )
    user_contact_2 = UserContactModel(
        user_id=user.id, value="+88005553535", type=ContactTypeEnum.PHONE, active=True, is_favorite=False
    )

    session.add_all([user_contact_1, user_contact_2])
    await session.commit()

    await session.delete(user_contact_1)
    await session.delete(user_contact_2)
    await session.commit()

    await session.delete(user)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_fail_user_contacts_index_ck -v -s
@pytest.mark.asyncio
async def test_fail_user_contacts_index_ck(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(user)
    await session.flush()

    user_contact_1 = UserContactModel(
        user_id=user.id, value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True
    )
    user_contact_2 = UserContactModel(
        user_id=user.id, value="+88005553535", type=ContactTypeEnum.PHONE, active=True, is_favorite=True
    )
    await session.commit()

    with pytest.raises(IntegrityError) as e:
        session.add_all([user_contact_1, user_contact_2])
        await session.commit()
    assert "ix_uq_user_id_is_favorite" in str(e.value)
    await session.rollback()

    await session.delete(user)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_fail_user_contacts_uniq_ck -v -s
@pytest.mark.asyncio
async def test_fail_user_contacts_uniq_ck(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    session.add(user)
    await session.commit()

    user_contact_1 = UserContactModel(
        user_id=user.id, value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True
    )
    user_contact_2 = UserContactModel(
        user_id=user.id, value="test@gmail.com", type=ContactTypeEnum.GMAIL, active=True, is_favorite=False
    )
    with pytest.raises(IntegrityError) as e:
        session.add_all([user_contact_1, user_contact_2])
        await session.commit()
    assert "uq_user_contact_user_id_values_types" in str(e.value)
    await session.rollback()

    await session.delete(user)
    await session.commit()


# pytest tests/main/user/test_user_contact.py::test_user_contact_set_favorite_ok -v -s
@pytest.mark.asyncio
async def test_user_contact_set_favorite_ok(session: AsyncSession):
    user = UserModel(id="Test", username="Test", active=True, language=DEFAULT_TEST_LANGUAGE)

    session.add(user)
    await session.commit()

    user_contact_current_favorite = UserContactModel(
        user_id=user.id, value="old", type=ContactTypeEnum.GMAIL, active=True, is_favorite=True
    )

    user_contact_new_favorite = UserContactModel(
        user_id=user.id, value="new", type=ContactTypeEnum.GMAIL, active=True, is_favorite=False
    )

    session.add_all([user_contact_current_favorite, user_contact_new_favorite])
    await session.commit()

    current_favorite_set_unfavorite = (
        update(UserContactModel)
        .where(UserContactModel.id == user_contact_current_favorite.id)
        .values(is_favorite=False)
        .returning(UserContactModel)
    )

    new_favorite = (
        update(UserContactModel)
        .where(UserContactModel.id == user_contact_new_favorite.id)
        .values(is_favorite=True)
        .returning(UserContactModel)
    )

    res_unfavorite = await session.scalar(current_favorite_set_unfavorite)
    res_favorite = await session.scalar(new_favorite)
