
import unittest

from mojo.xmods.xconvert import (
    safe_as_bytes,
    safe_as_str
)

class TestStrToByteConversions(unittest.TestCase):

    def test_str_to_bytes_conversion(self):
        buffer = safe_as_bytes("Test String")
        assert isinstance(buffer, bytes), "Expected conversion to bytes"
        return

class TestByteToStrConversions(unittest.TestCase):

    def test_str_to_bytes_conversion(self):
        buffer = safe_as_str(b"Test String")
        assert isinstance(buffer, str), "Expected conversion to str"
        return

if __name__ == '__main__':
    unittest.main()
