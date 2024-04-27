from enum import Enum


class FormyType(Enum):
    Y = "yes"
    N = "no"
    UNKNOWN = "unknown"

    @staticmethod
    def decode(value):
        for member in FormyType:
            if member.value == value:
                return member
        return FormyType.UNKNOWN


class IonType(Enum):
    H = ("H", 1.008)
    NA = ("Na", 22.990)
    K = ("K", 39.098)
    UNKNOWN = ("unknown", 0)

    def __init__(self, text, weight):
        self.text = text
        self.weight = weight

    @staticmethod
    def decode(value):
        for member in IonType:
            if member.text == value:
                return member
        return IonType.UNKNOWN
