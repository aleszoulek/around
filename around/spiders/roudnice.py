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
        events = hxs.select("//div[@id='floatbug']/div/div")
        for event in events:
            if not event.select("h3"):
                continue
            yield event

    def parse_value(self, node):
        name = node.select("a/@name").extract()[0]
        data = node.select("a/span[@class='datum']/text()").extract()[0].split('|')
        if data[1].endswith('         '):
            venue = data[2].strip()
        else:
            venue = data[1].strip()

        return {
            'id': name,
            'name': node.select('h3/span/text()').extract()[0],
            'description': ''.join(node.select('text()').extract()).strip(),
            'link': '%s#%s' % (self.start_urls[0], name),
            'venue': venue,
        }

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        event_items = []
        for event in self.get_nodes(hxs):
            event_item = EventItem()
            event_item.update(self.parse_value(event))
            event_item['source'] = self.name
            event_items.append(event_item)
        return event_items

