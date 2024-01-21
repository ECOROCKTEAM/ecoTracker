import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.enum.user.contact import ContactTypeEnum
from src.data.models.user.contact import ContactModel
from src.data.models.user.user import UserContactModel, UserModel
from tests.fixtures.const import DEFAULT_TEST_LANGUAGE


# pytest tests/main/user/db/test_db.py::test_user_contacts_ok -v -s
@pytest.mark.asyncio
async def test_user_contacts_ok(session: AsyncSession):
    user = UserModel(id="Lana Del Rey", username="Roma", password="", active=True, language=DEFAULT_TEST_LANGUAGE)
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
    user = UserModel(id="Lana Del Rey", username="Roma", password="", active=True, language=DEFAULT_TEST_LANGUAGE)
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
    user = UserModel(id="Lana Del Rey", username="Roma", password="", active=True, language=DEFAULT_TEST_LANGUAGE)
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
