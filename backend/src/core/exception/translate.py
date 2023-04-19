from src.core.exception.base import DomainError


class TranslateError(DomainError):
    msg_template = "not found translate for languages: {languages}"
