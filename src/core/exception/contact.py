from src.core.exception.base import DomainError, EntityNotActive


class ContactNotActive(EntityNotActive):
    msg_template = "Contact={id} not active"


class ContactIsFavoriteError(DomainError):
    msg_template = "Contact={value} is favorite"


class ContactIsNotActiveError(DomainError):
    msg_template = "Contact={valie} active error"
