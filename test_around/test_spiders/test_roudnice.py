from nose import tools
from unittest import TestCase

from scrapy.selector import HtmlXPathSelector

from around.spiders import roudnice

class TestRoudniceSpider(TestCase):
    def setUp(self):
        self.html = '''
        <body>
        <ul>
            <li>one</li>
            <li>two</li>
        </ul>
        </body>
        '''

    def test_get_nodes_will_get_two_nodes(self):
        spider = roudnice.RoudniceSpider()
        xhs = HtmlXPathSelector(text=self.html)
        tools.assert_equals(2, len(list(spider.get_nodes(xhs))))

    def test_parse_value_get_one_and_two_strings(self):
        spider = roudnice.RoudniceSpider()
        xhs = HtmlXPathSelector(text=self.html)
        nodes = list(spider.get_nodes(xhs))
        tools.assert_equals('one', spider.parse_value(nodes[0]))
        tools.assert_equals('two', spider.parse_value(nodes[-1]))

