import asyncio
from cgi import test
import logging
import logging.config
import os
from pathlib import Path
import time
from typing import AsyncGenerator, Generator, Optional
import pytest
import pytest_asyncio
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.database.base import create_async_engine, create_session_factory
from testcontainers.postgres import PostgresContainer  # type: ignore

ROOT_DIR = Path(os.getcwd())
BACKUP_PATH = "tests/dumps/backup.sql"


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:12", port=5432, dbname="ecodb", user="test")
    try:
        postgres.start()
        postgres_url = postgres.get_connection_url()
        print(f"postgres url: {postgres_url}")
        yield postgres_url
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig(ROOT_DIR / "alembic.ini")
    alembic_cfg.set_main_option(
        "script_location",
        str(ROOT_DIR / "src" / "application" / "database" / "migrations"),
    )
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture(scope="session")
def upgrade_schema_db(alembic_config: AlembicConfig):
    alembic_upgrade(alembic_config, "head")


@pytest.fixture(scope="module")
def sql_dump_stmts() -> Optional[list[str]]:
    if not os.path.exists(BACKUP_PATH):
        print(f"Not found dump file by {BACKUP_PATH=}!")
        return []
    with open(BACKUP_PATH, "r") as file:
        content = file.readlines()
    stmts: list[str] = []
    for line in content:
        if (
            line.startswith("--")
            or line.startswith(" ")
            or line == "\n"
        ):
            continue
        line = line.strip().replace("\n", "")
        stmts.append(line)
    print(f"Read from dump: {len(stmts)} rows")
    return stmts


@pytest.fixture(scope="module")
def pool(postgres_url: str, sql_dump_stmts, event_loop) -> Generator[async_sessionmaker[AsyncSession], None, None]:
    sync_engine = create_engine(url=postgres_url)
    connection = sync_engine.raw_connection()
    cursor = connection.cursor()
    for stmt in sql_dump_stmts:
        print(stmt)
        cursor.execute(stmt)
    connection.commit()
    connection.close()
    engine = create_async_engine(url=postgres_url.replace("psycopg2", "asyncpg"))
    factory = create_session_factory(engine=engine)
    yield factory
    # close_all_sessions()


@pytest_asyncio.fixture(scope="function")
async def session(pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session:
        yield session
