import os
import sys
import unittest

if sys.version_info >= (3, 3):
    # noinspection PyUnresolvedReferences
    from unittest import mock
else:
    # noinspection PyUnresolvedReferences
    import mock

from lib.utils.logger import Logger


@unittest.skip("not working with tox yet")  # TODO
class LoggerTest(unittest.TestCase):
    def test_givenMockedGetInstance_whenGetInstance_assertFileNotCreated(self):
        with mock.patch("lib.utils.logger.Logger.get_instance", return_value=mock.MagicMock()):
            _out = Logger.get_instance(__name__)
            self.assertFalse(os.path.exists(Logger.get_log_path()))
        return

    def test_givenLogFileTestDir_whenLog_assertLoggedCustomLogFile(self):
        log_path = os.path.join(os.path.dirname(__file__), "cinema.home.log")
        message1 = "This is a temporary test log message!"
        message2 = "Testing if these lines are logged to a custom file.."

        with mock.patch.object(Logger, 'get_log_path', return_value=log_path):
            _out = Logger.get_instance(__name__)
            _out.info(message1)
            _out.info(message2)
            _out.close()

        with open(log_path) as file:
            content = file.read().splitlines()
        os.remove(log_path)
        self.assertTrue(message1 in content[0])
        self.assertTrue(message2 in content[1])
        return


if __name__ == '__main__':
    unittest.main()
