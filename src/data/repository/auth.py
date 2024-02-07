from src.core.dto.auth.firebase import UserIdentity
from src.core.exception.base import AuthError
from src.core.interfaces.auth.firebase import IFirebaseApplication
from src.core.interfaces.repository.auth import IAuthProviderRepository


class AuthProviderRepository(IAuthProviderRepository):
    def __init__(self, firebase_app: IFirebaseApplication) -> None:
        self._fb_app = firebase_app

    async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity:
        try:
            token_identity = await self._fb_app.verify_token(token=token, check_revoked=check_revoked)
        except Exception as e:
            raise AuthError(msg=f"Error on verify token: {e}") from e
        try:
            user_identity = await self._fb_app.get_user(id=token_identity.user_id)
        except Exception as e:
            raise AuthError(msg=f"Error on get user by id={token_identity.user_id}: {e}") from e
        return user_identity
