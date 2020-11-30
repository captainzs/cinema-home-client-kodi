import sys
import unittest

from lib.utils import interpreter

if sys.version_info >= (3, 3):
    # noinspection PyUnresolvedReferences
    from unittest import mock
else:
    # noinspection PyUnresolvedReferences
    import mock


class InterpreterTest(unittest.TestCase):
    def test_givenOver1000MB_assertString(self):
        readable = interpreter.bytes_2_readable(1056534691)
        self.assertEqual("1007.6 MB", readable)
        return


if __name__ == '__main__':
    unittest.main()
