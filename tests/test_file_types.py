from modules.enums.file_types import SupportedFileType
import pytest


def test_is_supported_true():
    assert SupportedFileType.is_supported("csv") is True
    assert SupportedFileType.is_supported("pdf") is False


def test_is_supported_false():
    assert SupportedFileType.is_supported("test") is False
    assert SupportedFileType.is_supported("mp4") is False
