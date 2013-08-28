from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from around.items import EventItem

class DobrichoviceSpider(BaseSpider):
    name = "dobrichovice"
    allowed_domains = ["dobrichovice.cz"]
    start_urls = [
        'http://www.dobrichovice.cz/kultura/kultura-v-dobrichovicich/',
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        events = hxs.select("//div[@class='readable_list']//div[@class='item']")
        event_items = []
        for event in events:
            event_item = EventItem()
            event_item['name'] = event.select('h3/a/text()').extract()[0]
            event_item['venue'] = event.select("dl[@class='misto readable_item readable_pause']").select('dd/text()').extract()[0]
            event_item['source'] = self.name
            event_item['description'] = event.select("p[@class='popis readable_item']/text()").extract()[0]
            event_item['link'] = 'http://www.dobrichovice.cz' + event.select('h3/a/@href').extract()[0]
            event_item['id'] = event.select("a/@name").extract()[0]
            event_items.append(event_item)
        return event_items

