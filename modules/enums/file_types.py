from enum import Enum


class SupportedFileType(Enum):
    csv = 1,
    json = 2,
    yaml = 3

    @classmethod
    def is_supported(cls, extension):
        return extension in cls.__members__
