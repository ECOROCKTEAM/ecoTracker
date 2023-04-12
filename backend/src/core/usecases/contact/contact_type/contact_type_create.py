from dataclasses import dataclass

from src.core.interfaces.base import BaseAbstractRepo


@dataclass
class SuccessResult:
    pass


@dataclass
class FailOperation:
    message: str


class ContactTypeCreateUC:

    def __init__(self, repo: BaseAbstractRepo) -> None:
        self.repo = repo