from nose import tools
from unittest import TestCase
from os import path

from scrapy.selector import HtmlXPathSelector

from around.spiders import roudnice
import test_around

html = path.join(path.dirname(test_around.__file__), 'data', 'roudnice-130912-2324.html')
html = open(html).read()

class TestRoudniceSpider(TestCase):
    def setUp(self):
        self.html = html

    def test_get_nodes_get_seventy_nodes(self):
        # this info comes from the shell::
        #   links -dump test_around/data/roudnice-130912-2324.html | \
        #   grep -- '---------------------------------------------' | wc -l
        spider = roudnice.RoudniceSpider()
        xhs = HtmlXPathSelector(text=self.html)
        tools.assert_equals(70, len(list(spider.get_nodes(xhs))))

    def test_parse_value_with_just_venue_only_get_proper_data(self):
        spider = roudnice.RoudniceSpider()
        xhs = HtmlXPathSelector(text=self.html)
        nodes = list(spider.get_nodes(xhs))
        expected = {
            'id': '4789',
            'link': 'http://www.roudnicenl.cz/mesto/kalendar-akci#4789',
            'name': 'Letci z hlubin',
            'venue': u'Pod\u0159ipsk\xe9 muzeum',
            'description': u'V\xfdstava  p\u0159ibli\u017euje v\xfdznamnou bitvu mezi americk\xfdm letectvem a n\u011bmeckou Lufthaffe z roku 1944 nad Kru\u0161n\xfdmi horami a prezentuje autentick\xe9 expon\xe1ty v podob\u011b relikt\u016f sest\u0159elen\xfdch letadel stejn\u011b jako dal\u0161\xed historick\xe9 re\xe1lie vztahuj\xedc\xed se k t\xe9to v\xfdznamn\xe9 ud\xe1losti 2. sv\u011btov\xe9 v\xe1lky.\r\n\r\nVernis\xe1\u017e v\xfdstavy: 8. 4. v 17.30 hodin.',
        }
        tools.assert_equals(expected, spider.parse_value(nodes[0]))

    def test_parse_value_with_time_and_more_info_get_proper_data(self):
        spider = roudnice.RoudniceSpider()
        xhs = HtmlXPathSelector(text=self.html)
        nodes = list(spider.get_nodes(xhs))
        expected = {
            'id': '4910',
            'link': 'http://www.roudnicenl.cz/mesto/kalendar-akci#4910',
            'name': u'Podzimn\xed tvo\u0159en\xed z list\u016f',
            'venue': u'Galerie modern\xedho um\u011bn\xed',
            'description': u'Sobotn\xed v\xfdtvarn\xe1 d\xedlna pro dosp\u011bl\xe9 a rodi\u010de s d\u011btmi. Z nasb\xedran\xfdch list\u016f budeme vytv\xe1\u0159et kol\xe1\u017ee, podzimn\xed v\u011bnce nebo r\u016f\u017ee.',
        }
        tools.assert_equals(expected, spider.parse_value(nodes[-3]))

