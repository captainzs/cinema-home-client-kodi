import unittest
import xbmc


class XbmcTest(unittest.TestCase):
    def test_imports(self):
        xbmc.log("Test")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
