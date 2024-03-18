import os

from src.application.auth.firebase import (
    FirebaseApplication,
    FirebaseApplicationSingleton,
)
from src.application.settings import settings
from src.core.dto.auth.firebase import ProviderIdentity, TokenIdentity, UserIdentity
from src.core.interfaces.auth.firebase import IFirebaseApplication


# pytest tests/tmain/firebase/test_firebase_app.py::test_app_singleton -v -s
def test_app_singleton():
    app = FirebaseApplicationSingleton(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    app.setup()
    app_id = id(app)
    app2 = FirebaseApplicationSingleton(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    assert app2._is_setup is True
    app2_id = id(app2)
    assert app_id == app2_id


# pytest tests/tmain/firebase/test_firebase_app.py::test_app_default -v -s
def test_app_default():
    app = FirebaseApplication(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    app.setup()
    app_id = id(app)
    app2 = FirebaseApplication(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    assert app2._is_setup is False
    app2_id = id(app2)
    assert app_id != app2_id


# Tests commented bcs need deps from env

# # pytest tests/main/auth/test_firebase_app.py::test_firebase_verify_token -v -s
# async def test_firebase_verify_token(firebase_app: IFirebaseApplication):
#     token = os.environ.get("FB_USER_TOKEN")
#     if token is None:
#         raise NotImplementedError("FB token not set for test")
#     token_identity = await firebase_app.verify_token(token=token)
#     assert isinstance(token_identity, TokenIdentity)


# # pytest tests/main/auth/test_firebase_app.py::test_firebase_get_user -v -s
# async def test_firebase_get_user(firebase_app: IFirebaseApplication):
#     token = os.environ.get("FB_USER_TOKEN")
#     if token is None:
#         raise NotImplementedError("FB token not set for test")
#     token_identity = await firebase_app.verify_token(token=token)
#     user_identity = await firebase_app.get_user(id=token_identity.user_id)
#     assert isinstance(user_identity, UserIdentity)
#     assert isinstance(user_identity.provider, ProviderIdentity)
