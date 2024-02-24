import asyncio

import click

from src.cli.common import (
    get_mock_auth_provider,
    get_session_factory,
    read_develop_json,
)
from src.core.usecases.user.user_me import UserMeUsecase
from src.data.unit_of_work import SqlAlchemyUnitOfWork


@click.group()
def develop():
    ...


@develop.command()
def load_users() -> None:
    dev_data = read_develop_json()
    develop_user_list = dev_data["develop_user_list"]
    auth_provider = get_mock_auth_provider(user_identity_list=develop_user_list)
    session_factory = get_session_factory()
    for user_identity in develop_user_list:
        uow = SqlAlchemyUnitOfWork(session_factory)
        uc = UserMeUsecase(uow=uow, auth_provider=auth_provider)
        asyncio.get_event_loop().run_until_complete(uc(token=user_identity["id"]))
