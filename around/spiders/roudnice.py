import datetime

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from around.items import EventItem

class RoudniceSpider(BaseSpider):
    name = "roudnice"
    allowed_domains = ["roudnicenl.cz"]
    start_urls = [
        'http://www.roudnicenl.cz/mesto/kalendar-akci',
    ]
    default_coords = (50.4241786, 14.2602997)

    def get_nodes(self, hxs):
        events = hxs.select("//div[@id='floatbug']/div/div")
        for event in events:
            if not event.select("h3"):
                continue
            yield event

    def parse_date(self, date, time=None):
        if '-' in date:
            date_from, date_to = date.split('-')
            date_from = datetime.datetime.strptime(date_from.strip(), '%d. %m. %Y').date()
            date_to = datetime.datetime.strptime(date_to.strip(), '%d. %m. %Y').date()
        else:
            date = datetime.datetime.strptime(date.strip(), '%d. %m. %Y').date()
            date_from, date_to = date, date

        time_from, time_to = None, None
        if time:
            time = datetime.datetime.strptime(time, '%H:%M').time()
            time_from, time_to = time, time

        return date_from, date_to, time_from, time_to

    def parse_value(self, node):
        name = node.select("a/@name").extract()[0]
        data = node.select("a/span[@class='datum']/text()").extract()[0].split('|')

        date = data[0]
        time = None
        if data[1].endswith('         '):
            venue = data[2].strip()
            time = data[1].strip()
        else:
            venue = data[1].strip()

        date_from, date_to, time_from, time_to = self.parse_date(date, time)

        return {
            'id': name,
            'date_from': date_from,
            'date_to': date_to,
            'time_from': time_from,
            'time_to': time_to,
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

