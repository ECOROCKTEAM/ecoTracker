from src.core.exception.base import RepoError

class ContactValueError(RepoError):
    msg = "Value={value} is not correct"