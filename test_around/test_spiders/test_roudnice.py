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
        # TODO: add venue, description
        expected = {
            'id': '4789',
            'link': 'http://www.roudnicenl.cz/mesto/kalendar-akci#4789',
            'name': 'Letci z hlubin',
        }
        got = spider.parse_value(nodes[0])
        tools.assert_equals(expected['id'], got['id'])
        tools.assert_equals(expected['link'], got['link'])
        tools.assert_equals(expected['name'], got['name'])

    def test_parse_value_with_more_complicated_data(self):
        # TODO: ^
        pass

