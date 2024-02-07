import pytest

from src.core.entity.user import UserCreateDTO
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotCreated, EntityNotFound
from src.core.interfaces.repository.user.user import IUserRepository
from tests.dataloader import dataloader


# pytest tests/tmain/repository/test_user.py::test_get_ok -v -s
@pytest.mark.asyncio
async def test_get_ok(dl: dataloader, repo_user: IUserRepository):
    print()
    # Arrange
    user_model = await dl.user_loader.create()
    # Act
    user = await repo_user.get(id=user_model.id)
    # Assert
    assert user.id == user_model.id
    assert user.active == user_model.active
    assert user.language == user_model.language


# pytest tests/tmain/repository/test_user.py::test_get_not_found -v -s
@pytest.mark.asyncio
async def test_get_not_found(dl: dataloader, repo_user: IUserRepository):
    print()
    # Arrange
    target_id = "aboba"
    # Act & Assert
    with pytest.raises(EntityNotFound):
        await repo_user.get(id=target_id)


# pytest tests/tmain/repository/test_user.py::test_create_ok -v -s
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "create_obj",
    [
        UserCreateDTO(id="aboba", username="aboba", active=True, language=LanguageEnum.EN),
        UserCreateDTO(id="boba", username="boba", active=False, language=LanguageEnum.RU),
    ],
)
async def test_create_ok(dl: dataloader, repo_user: IUserRepository, create_obj: UserCreateDTO):
    print()
    # Act
    user = await repo_user.create(obj=create_obj)
    # Assert
    assert user.id == create_obj.id
    assert user.username == create_obj.username
    assert user.active == create_obj.active
    assert user.language == create_obj.language


# pytest tests/tmain/repository/test_user.py::test_create_uniq_fail_by_id -v -s
@pytest.mark.asyncio
async def test_create_uniq_fail_by_id(dl: dataloader, repo_user: IUserRepository):
    print()
    # Arrange
    user_model = await dl.user_loader.create()
    # Act & Assert
    with pytest.raises(EntityNotCreated) as e:
        await repo_user.create(
            obj=UserCreateDTO(id=user_model.id, username="something", active=True, language=LanguageEnum.RU)
        )
    assert "Uniq failed" in str(e.value)


# pytest tests/tmain/repository/test_user.py::test_create_uniq_fail_by_username -v -s
@pytest.mark.asyncio
async def test_create_uniq_fail_by_username(dl: dataloader, repo_user: IUserRepository):
    print()
    # Arrange
    duplicate_username = "amogus"
    await dl.user_loader.create(username=duplicate_username)
    # Act & Assert
    with pytest.raises(EntityNotCreated) as e:
        await repo_user.create(
            obj=UserCreateDTO(id="boba", username=duplicate_username, active=True, language=LanguageEnum.RU)
        )
    assert "Uniq failed" in str(e.value)


# # pytest tests/tmain/repository/test_user.py::test_update_ok -v -s
# @pytest.mark.asyncio
# async def test_update_ok(dl: dataloader, repo_user: IUserRepository):
#     print()
#     # Arrange

#     # Act

#     # Assert
