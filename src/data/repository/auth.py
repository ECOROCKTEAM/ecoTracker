from src.core.dto.auth.firebase import UserFirebase
from src.core.enum.auth.providers import AuthProviderEnum
from src.core.interfaces.auth.firebase import IFirebaseApplication
from src.core.interfaces.repository.auth import IAuthProviderRepository


def firebase_user_to_dto(obj) -> UserFirebase:
    return UserFirebase(
        id=obj.id,
        name=obj.display_name,
        active=not obj.disabled,
        pic=obj.photo_url,
        firebase_app_name=obj.aud,
        auth_time=obj.auth_time,
        email=obj.email,
        provider=AuthProviderEnum.GOOGLE,
    )


class AuthProviderRepository(IAuthProviderRepository):
    def __init__(self, firebase_app: IFirebaseApplication) -> None:
        self._fb_app = firebase_app

    async def get_firebase_user_by_token(self, token: str, check_revoked: bool = True) -> UserFirebase:
        decoded_token = await self._fb_app.verify_token(token=token, check_revoked=check_revoked)
        user = await self._fb_app.get_user(id=decoded_token["uid"])
        return firebase_user_to_dto(user)
