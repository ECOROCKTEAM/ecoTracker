from __future__ import annotations
import abc
from src.core.interfaces.repository.community.community import IRepositoryCommunity


class IUnitOfWork(abc.ABC):
    @property
    @abc.abstractmethod
    def community(self) -> IRepositoryCommunity:
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> IUnitOfWork:
        ...

    @abc.abstractmethod
    async def __aexit__(self, *args):
        ...

    @abc.abstractmethod
    async def commit(self):
        ...

    @abc.abstractmethod
    async def rollback(self):
        ...
