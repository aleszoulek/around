from scrapy.spider import BaseSpider

from around.items import EventItem

class RoudniceSpider(BaseSpider):
    name = "roudnice"

    def get_nodes(self, hxs):
        for n in hxs.select('//ul/li'):
            yield n

    def parse_value(select, node):
        return node.select('text()').extract()[0]

    def parse(self, response):
        return [EventItem()]

