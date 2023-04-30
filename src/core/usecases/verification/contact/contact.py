from src.core.dto.user.contact import ContactTypeDTO
from src.core.exception.contact import ContactValueError


async def contact_value_type_check(*, contact: str, type: ContactTypeDTO) -> bool:
    """Checking if the value matches the type.

    Args:
        contact (str): string of contact
        type (ContactTypeDTO): DTO of contact type object

    Raises:
        ContactValueError: Contact doesn't type error

    Returns:
        bool: bool
    """

    # В pydantic есть специальный тип для проверки поля на то, что это mail. Но мы его не будем пользовать.
    # Сделал в примитиве (грубом (слива спелая...)). Жду комментария по этому делу

    if type.enum.PHONE and not contact.startswith("+"):
        raise ContactValueError(value=contact)
    if type.enum.MAIL and "@" not in contact:
        raise ContactValueError(value=contact)

    return True
