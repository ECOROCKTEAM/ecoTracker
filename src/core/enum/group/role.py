from src.core.enum.base.translation import TranslationEnum


class GroupRoleEnum(str, TranslationEnum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"
    BLOCKED = "BLOCKED"
