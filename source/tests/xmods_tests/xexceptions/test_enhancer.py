import unittest

from mojo.xmods.xtraceback import (
    enhance_exception,
    format_exception
)

class TestError(Exception):
    """
        This is a test error used for testing the exceptionator.
    """

def failing_function():
    raise TestError("This is a test error")

class TestEnhancer(unittest.TestCase):

    def test_enhance_exception(self):

        try:
            failing_function()
        except TestError as terr:
            enhance_exception(terr, "This is some extra content.", "BLAH")

            tblines = format_exception(terr)

            for line in tblines:
                print(line)

        return

if __name__ == '__main__':
    unittest.main()
