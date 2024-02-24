from src.application.auth.firebase import FirebaseApplicationSingleton
from src.application.settings import settings
from src.core.interfaces.repository.auth import IAuthProviderRepository
from src.data.repository.auth import AuthProviderRepository


def get_auth_provider() -> IAuthProviderRepository:
    firebase_app = FirebaseApplicationSingleton(
        name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH
    )
    return AuthProviderRepository(firebase_app=firebase_app)
