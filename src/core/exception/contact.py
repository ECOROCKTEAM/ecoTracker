from src.core.exception.base import RepoError


class ContactValueError(RepoError):
    msg_template = "Value={value} is not correct"


class ContactIsFavoriteError(RepoError):
    msg_template = "Contact={value} is favorite"


class ContactIsNotActiveError(RepoError):
    msg_template = "Contact={valie} active error"
