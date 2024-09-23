from enum import Enum


class SupportedFileType(Enum):
    csv = 1,
    json = 2,
    xml = 3,
    yaml = 4

    @classmethod
    def is_supported(cls, extension):
        return extension in cls.__members__
