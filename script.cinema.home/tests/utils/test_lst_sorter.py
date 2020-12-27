import sys
import unittest

from lib.models.json.image_info import Image
from lib.utils import lst_sorter

if sys.version_info >= (3, 3):
    # noinspection PyUnresolvedReferences
    from unittest import mock
else:
    # noinspection PyUnresolvedReferences
    import mock


class LstSorterTest(unittest.TestCase):
    def test_givenUrlsWithLanguages_assertOrderedByLanguagePriorities(self):
        images = [Image.of({"url": "url1", "iso639Id": "en"}),
                  Image.of({"url": "url2"}),
                  Image.of({"url": "url3", "iso639Id": "hu"}),
                  Image.of({"url": "url4", "iso639Id": "en"}),
                  Image.of({"url": "url5", "iso639Id": "es"}),
                  Image.of({"url": "url6", "iso639Id": "hu"}),
                  Image.of({"url": "url7"}),
                  Image.of({"url": "url8"}),
                  Image.of({"url": "url9", "iso639Id": "hu"}),
                  Image.of({"url": "url10", "iso639Id": "hu"}),
                  Image.of({"url": "url11", "iso639Id": "en"})]
        sorted_lst = lst_sorter.sort_arts(images, ["hu", None, "en"])
        self.assertEqual('url3', sorted_lst[0].get_url())
        self.assertEqual('url6', sorted_lst[1].get_url())
        self.assertEqual('url9', sorted_lst[2].get_url())
        self.assertEqual('url10', sorted_lst[3].get_url())
        self.assertEqual('url2', sorted_lst[4].get_url())
        self.assertEqual('url7', sorted_lst[5].get_url())
        self.assertEqual('url8', sorted_lst[6].get_url())
        self.assertEqual('url1', sorted_lst[7].get_url())
        self.assertEqual('url4', sorted_lst[8].get_url())
        self.assertEqual('url11', sorted_lst[9].get_url())
        self.assertEqual('url5', sorted_lst[10].get_url())
        return

    def test_givenUrlsWithLanguagesAndSameIsoTwice_assertOrderedByLanguagePriorities(self):
        images = [Image.of({"url": "url1", "iso639Id": "en"}),
                  Image.of({"url": "url2"}),
                  Image.of({"url": "url3", "iso639Id": "hu"}),
                  Image.of({"url": "url4", "iso639Id": "en"}),
                  Image.of({"url": "url5", "iso639Id": "es"}),
                  Image.of({"url": "url6", "iso639Id": "hu"}),
                  Image.of({"url": "url7"}),
                  Image.of({"url": "url8"}),
                  Image.of({"url": "url9", "iso639Id": "hu"}),
                  Image.of({"url": "url10", "iso639Id": "hu"}),
                  Image.of({"url": "url11", "iso639Id": "en"})]
        sorted_lst = lst_sorter.sort_arts(images, ["en", "en"])
        self.assertEqual('url1', sorted_lst[0].get_url())
        self.assertEqual('url4', sorted_lst[1].get_url())
        self.assertEqual('url11', sorted_lst[2].get_url())
        self.assertEqual('url2', sorted_lst[3].get_url())
        self.assertEqual('url3', sorted_lst[4].get_url())
        self.assertEqual('url5', sorted_lst[5].get_url())
        self.assertEqual('url6', sorted_lst[6].get_url())
        self.assertEqual('url7', sorted_lst[7].get_url())
        self.assertEqual('url8', sorted_lst[8].get_url())
        self.assertEqual('url9', sorted_lst[9].get_url())
        self.assertEqual('url10', sorted_lst[10].get_url())
        return


if __name__ == '__main__':
    unittest.main()
