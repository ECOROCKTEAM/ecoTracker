from src.application.auth.firebase import FirebaseApplication
from src.application.settings import settings
from src.core.interfaces.auth.firebase import IFirebaseApplication


# pytest tests/main/auth/test_firebase_app.py::test_app_singleton -v -s
def test_app_singleton():
    app = FirebaseApplication(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    app.setup()
    app_id = id(app)
    app2 = FirebaseApplication(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
    assert app2._was_init
    app2_id = id(app2)
    assert app_id == app2_id


# pytest tests/main/auth/test_firebase_app.py::test_firebase_verify_token -v -s
async def test_firebase_verify_token(firebase_app: IFirebaseApplication):
    token_data: dict = await firebase_app.verify_token(token="")
    print(token_data)
    # TODO
    ...
