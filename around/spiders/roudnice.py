from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from around.items import EventItem

class RoudniceSpider(BaseSpider):
    name = "roudnice"
    allowed_domains = ["roudnicenl.cz"]
    start_urls = [
        'http://www.roudnicenl.cz/mesto/kalendar-akci',
    ]

    def get_nodes(self, hxs):
        for n in hxs.select('//ul/li'):
            yield n

    def parse_value(select, node):
        return node.select('text()').extract()[0]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        events = hxs.select("//div[@id='floatbug']/div/div")
        event_items = []
        for event in events:
            if not event.select("h3"):
                continue

            name = event.select("a/@name").extract()[0]
            data = event.select("a/span[@class='datum']/text()").extract()[0].split('|')

            event_item = EventItem()
            event_item['name'] = event.select('h3/span/text()').extract()[0]
            event_item['source'] = self.name
            event_item['description'] = ''.join(event.select('text()').extract()).strip()
            event_item['link'] = '%s#%s' % (self.start_urls[0], name)
            event_item['id'] = name

            if data[1].endswith('         '):
                event_item['venue'] = data[2].strip()
            else:
                event_item['venue'] = data[1].strip()

            event_items.append(event_item)
        return event_items

