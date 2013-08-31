from datetime import datetime, date, time
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
            (
                event_item['date_from'],
                event_item['date_to'],
                event_item['time_from'],
                event_item['time_to'],
            ) = self.parse_date(
                event.select("dl[@class='data readable_item']").select('dd/text()')[0].extract()
            )
            event_item['name'] = event.select('h3/a/text()').extract()[0]
            event_item['venue'] = event.select("dl[@class='misto readable_item readable_pause']").select('dd/text()').extract()[0]
            event_item['source'] = self.name
            event_item['description'] = event.select("p[@class='popis readable_item']/text()").extract()[0]
            event_item['link'] = 'http://www.dobrichovice.cz' + event.select('h3/a/@href').extract()[0]
            event_item['id'] = event.select("a/@name").extract()[0]
            event_items.append(event_item)
        return event_items

    def parse_date(self, raw):
        raw = raw.strip()
        dt = datetime.strptime(raw, '%d. %m. %Y')
        return dt.date(), dt.date(), None, None

        #return date.today(), date.today(), None, None
        return date.today(), date.today(), datetime.now().time(), datetime.now().time()

