import pytest
from sqlalchemy import and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.user.contact import ContactTypeEnum
from src.core.exception.base import EntityNotFound
from src.data.models.user.contact import ContactModel
from src.data.models.user.user import UserContactModel, UserModel
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE


# pytest tests/main/user/db/test_db.py::test_user_create_with_contact -v -s
@pytest.mark.asyncio
async def test_user_create_with_contact(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    contact = ContactModel(value=user.username, type=ContactTypeEnum.GMAIL)
    session.add_all([user, contact])
    await session.commit()
    user_contact = UserContactModel(user_id=user.id, contact_id=contact.id, active=True, is_favorite=True)
    session.add(user_contact)
    await session.commit()

    await session.delete(user_contact)
    await session.commit()

    await session.delete(user)
    await session.delete(contact)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_user_contact_set_favorite -v -s
@pytest.mark.asyncio
async def test_user_contact_set_favorite(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    contact_1 = ContactModel(value="some@gmail.com", type=ContactTypeEnum.GMAIL)

    contact_2 = ContactModel(value="42", type=ContactTypeEnum.PHONE)
    session.add_all([user, contact_1, contact_2])
    await session.flush()

    user_contact_1 = UserContactModel(user_id=user.id, contact_id=contact_1.id, active=True, is_favorite=True)
    user_contact_2 = UserContactModel(user_id=user.id, contact_id=contact_2.id, active=True, is_favorite=False)

    session.add_all([user_contact_1, user_contact_2])
    await session.commit()

    stmt_1 = (
        update(UserContactModel)
        .where(and_(UserContactModel.user_id == user.id, UserContactModel.contact_id == user_contact_1.id))
        .values(is_favorite=False)
        .returning(UserContactModel)
    )
    set_favorite_as_unfavorite = await session.scalar(statement=stmt_1)
    if not set_favorite_as_unfavorite:
        raise EntityNotFound(msg="")
    stmt_2 = (
        update(UserContactModel)
        .where(and_(UserContactModel.user_id == user.id, UserContactModel.contact_id == user_contact_2.id))
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
    await session.delete(contact_1)
    await session.delete(contact_2)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_user_contacts_ok -v -s
@pytest.mark.asyncio
async def test_user_contacts_ok(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    contact_1 = ContactModel(value="some@gmail.com", type=ContactTypeEnum.GMAIL)

    contact_2 = ContactModel(value="42", type=ContactTypeEnum.PHONE)

    session.add_all([user, contact_1, contact_2])
    await session.flush()

    user_contact_1 = UserContactModel(user_id=user.id, contact_id=contact_1.id, active=True, is_favorite=True)
    user_contact_2 = UserContactModel(user_id=user.id, contact_id=contact_2.id, active=True, is_favorite=False)

    session.add_all([user_contact_1, user_contact_2])
    await session.commit()

    await session.delete(user_contact_1)
    await session.delete(user_contact_2)
    await session.commit()

    await session.delete(user)
    await session.delete(contact_1)
    await session.delete(contact_2)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_fail_user_contacts_index_ck -v -s
@pytest.mark.asyncio
async def test_fail_user_contacts_index_ck(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    contact_1 = ContactModel(value="some@gmail.com", type=ContactTypeEnum.GMAIL)
    contact_2 = ContactModel(value="42", type=ContactTypeEnum.PHONE)

    session.add_all([user, contact_1, contact_2])
    await session.flush()

    user_contact_1 = UserContactModel(user_id=user.id, contact_id=contact_1.id, active=True, is_favorite=True)
    user_contact_2 = UserContactModel(user_id=user.id, contact_id=contact_2.id, active=True, is_favorite=True)
    await session.commit()

    with pytest.raises(IntegrityError) as e:
        session.add_all([user_contact_1, user_contact_2])
        await session.commit()
    assert "ix_uq_user_id_is_favorite" in str(e.value)
    await session.rollback()

    await session.delete(user)
    await session.delete(contact_1)
    await session.delete(contact_2)
    await session.commit()


# pytest tests/main/user/db/test_db.py::test_fail_user_contacts_uniq_ck -v -s
@pytest.mark.asyncio
async def test_fail_user_contacts_uniq_ck(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", active=True, language=DEFAULT_TEST_LANGUAGE)
    contact_1 = ContactModel(value="some@gmail.com", type=ContactTypeEnum.GMAIL)
    contact_2 = ContactModel(value="42", type=ContactTypeEnum.PHONE)

    session.add_all([user, contact_1, contact_2])
    await session.flush()

    user_contact_1 = UserContactModel(user_id=user.id, contact_id=contact_1.id, active=True, is_favorite=True)
    user_contact_2 = UserContactModel(user_id=user.id, contact_id=contact_1.id, active=True, is_favorite=False)

    await session.commit()

    with pytest.raises(IntegrityError) as e:
        session.add_all([user_contact_1, user_contact_2])
        await session.commit()
    assert "user_contact_user_id_contact_id_key" in str(e.value)
    await session.rollback()

    await session.delete(user)
    await session.delete(contact_1)
    await session.delete(contact_2)
    await session.commit()
