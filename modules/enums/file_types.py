from enum import Enum


class SupportedFileType(Enum):
    xlsx = 1
    csv = 2
    json = 3
    raw = 4

    @classmethod
    def is_supported(cls, extension):
        return extension in cls.__members__
