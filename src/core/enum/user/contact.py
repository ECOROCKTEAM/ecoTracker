from src.core.enum.base.translation import TranslationEnum


class ContactTypeEnum(str, TranslationEnum):
    PHONE = "PHONE"
    MAIL = "MAIL"
    TELEGRAM = "TELEGRAM"
    WHATSAPP = "WHATSAPP"
    GMAIL = "GMAIL"
    FACEBOOK = "FACEBOOK"
    CUSTOM = "CUSTOM"
