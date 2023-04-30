from src.core.enum.base.translation import TranslationEnum


class CommunityRoleEnum(str, TranslationEnum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"
    BLOCKED = "BLOCKED"
