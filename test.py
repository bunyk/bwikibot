#coding=utf-8

from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from unittest import TestCase, main
import sys

from bwikibot.api import datetime2zulu, zulu2datetime

class Zulu(TestCase):
    def test_now(self):
        now = datetime.now().replace(microsecond=0)
        zulu = datetime2zulu(now)

        self.assertEqual(zulu2datetime(zulu), now)


from bwikibot.spell.corrector import correct
class TestCorrector(TestCase):
    def test_not_whole_word(self):
        self.assertEqual(correct('аргументами'), 'аргументами')

    def test_a_u(self):
        self.assertEqual(correct('аргумента'), 'аргументу')

from bwikibot.utils import parse_signature_time
class TestParseSignatureTime(TestCase):
    def test_correct(self):
        self.assertEqual(
            parse_signature_time('23:54, 13 листопада 2012 (UTC)'),
            datetime(2012, 11, 13, 23, 54)
        )

from bwikibot.utils import skip_boring_lines
class TestSkipBoringLines(TestCase):
    def test_not_boring(self):
        self.assertEqual(
            list(skip_boring_lines([0, 1, 0, 1], lambda x: x)),
            [0, 1, 0, 1]
        )

    def test_boring_inside(self):
        self.assertEqual(
            list(skip_boring_lines([0, 1, 1, 1, 0], lambda x: x, 2)),
            [0, 1, '...', 1, 0]
        )
    def test_boring_end(self):
        self.assertEqual(
            list(skip_boring_lines(range(10), lambda x: x, 3)),
            [0, 1, 2, 3, '...']
        )

from bwikibot.api import Wiki

class TestWikiClassesCreation(TestCase):
    def test_wiki(self):
        wiki = Wiki()
        wiki.namespaces_names = {
            1: 'File',
            2: 'User',
        }
        wiki.namespaces_ids = {
            'File': 1,
            'User': 2,
        }
        wiki.set_default_namespaces()
        file = wiki.file('asdf')
        page = wiki.page('asdf')

if __name__=='__main__':
    print('Testing on:', sys.version)
    main()
