class BaseError(Exception):
    msg_template = "{msg}"

    def __init__(self, **kwargs):
        self.msg = self.msg_template.format(**kwargs)
        super().__init__(self.msg)


class DomainError(BaseError):
    """"""


class RepoError(BaseError):
    """"""


class AuthError(DomainError):
    """"""


class PermissionError(DomainError):
    """"""


class EntityNotFound(DomainError):
    """"""


class EntityNotCreated(DomainError):
    """"""


class EntityNotDeleted(DomainError):
    """"""


class EntityAlreadyUsage(DomainError):
    """"""


class EntityNotActive(DomainError):
    """"""


class EntityNotChange(DomainError):
    """"""


class PrivacyError(DomainError):
    """"""


class LogicError(DomainError):
    """"""


class MaxAmountError(DomainError):
    """"""


class TranslateNotFound(DomainError):
    """"""
