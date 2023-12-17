from src.core.interfaces.repository.auth import IAuthProviderRepository


# pytest tests/main/auth/test_repository.py::test_get_firebase_user_by_token -v -s
async def test_get_firebase_user_by_token(auth_provider_repository: IAuthProviderRepository):
    # user = await auth_provider_repository.get_firebase_user_by_token(
    #     token=""
    # )
    # print(user)
    # TODO
    ...
