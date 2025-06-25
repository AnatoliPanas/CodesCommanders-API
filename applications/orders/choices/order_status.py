from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "Создан"
    CLOSE = "Закрыт"


    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]