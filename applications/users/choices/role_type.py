from enum import Enum

class RoleType(str, Enum):
    ADMIN = "Администратор"
    USER = "Пользователь"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]