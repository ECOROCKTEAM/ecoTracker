import asyncio

import firebase_admin
from firebase_admin import App, auth
from firebase_admin._user_mgt import UserRecord

from src.core.interfaces.auth.firebase import IFirebaseApplication


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


# TODO HANDLE ERRORS


@singleton
class FirebaseApplication(IFirebaseApplication):
    def __init__(self, name: str, secret_path: str) -> None:
        self._name = name
        self._secret_path = secret_path
        self._was_init = False
        self._app: App | None = None

    @property
    def name(self) -> str:
        return self._name

    async def verify_token(self, token: str, check_revoked: bool = True) -> dict:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, auth.verify_id_token, token, self._app, check_revoked)
        return data

    async def get_user(self, id: str) -> UserRecord:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, auth.get_user, id, self._app)
        return data

    def setup(self):
        if not self._was_init:
            credential = firebase_admin.credentials.Certificate(self._secret_path)
            # That create app in global firebase_admin scope..
            self._app = firebase_admin.initialize_app(credential=credential, name=self._name)
        self._was_init = True
