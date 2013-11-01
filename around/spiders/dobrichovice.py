import re
from datetime import datetime, date, time

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from around.items import EventItem

class DobrichoviceSpider(BaseSpider):
    name = "dobrichovice"
    allowed_domains = ["dobrichovice.cz"]
    start_urls = [
        'http://www.dobrichovice.cz/kultura/kultura-v-dobrichovicich/',
        'http://www.dobrichovice.cz/kultura/kultura-v-okolnich-obcich/',
    ]
    default_coords = (49.9262642, 14.2748719)

    def build_url(self, href):
        if href.startswith(('http://', 'https://')):
            return href
        return "http://www.dobrichovice.cz" + href

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
            event_item['venue'] = event.select("dl[@class='misto readable_item readable_pause']").select('dd//text()').extract()[0]
            event_item['source'] = self.name
            event_item['description'] = event.select("p[@class='popis readable_item']/text()").extract()[0]
            event_item['link'] = self.build_url(event.select('h3/a/@href').extract()[0])
            #event_item['id'] = event.select("a/@name").extract()[0]
            event_item['id'] = event.select("h3/a/@href").extract()[0]
            event_items.append(event_item)

        current_page = int(hxs.select("//div[@class='per_page']//strong/text()").extract()[0])
        other_pages = dict(
            (
                int(d.select('text()').extract()[0]),
                d.select('@href').extract()[0]
            )
            for d
            in set(hxs.select("//div[@class='per_page']//a"))
        )
        if current_page+1 in other_pages:
            event_items.append(Request(self.build_url(other_pages[current_page+1])))

        return event_items

    def parse_date(self, raw):
        raw = raw.strip()
        patterns = [
            r'''^\ *
                (?P<day_from>\d+)\.\ *(?P<month_from>\d+)\.\ *(?P<year_from>\d+)\ *$''', # 31. 2. 2013
            r'''^\ *
                (?P<day_from>\d+)\.\ *(?P<month_from>\d+)\.\ *(?P<year_from>\d+)
                \ *[^\ ]*\ od\ *(?P<hour_from>\d+):(?P<minute_from>\d+)
                \ *$''', # 3. 11. 2013 za\u010d\xe1tek od 16:00
            r'''^\ *
                (?P<day_from>\d+)\.\ *(?P<month_from>\d+)\.\ *(?P<year_from>\d+)
                \ *od\ *(?P<hour_from>\d+):(?P<minute_from>\d+)
                \ *do\ *(?P<hour_to>\d+):(?P<minute_to>\d+)
                \ *$''', # 22. 12. 2013 od 10:00 do 16:30
            r'''^\ *
                (?P<day_from>\d+)\.\ *(?P<month_from>\d+)\.\ *(?P<year_from>\d+)
                \ *od\ *(?P<hour_from>\d+):(?P<minute_from>\d+)
                \ *-\ *
                (?P<day_to>\d+)\.\ *(?P<month_to>\d+)\.\ *(?P<year_to>\d+)
                \ *do\ *(?P<hour_to>\d+):(?P<minute_to>\d+)
                \ *$''', # 1. 9. 2013 od 10:00 - 31. 10. 2013 do 16:00
            r'''^\ *
                (?P<day_from>\d+)\.\ *(?P<month_from>\d+)\.
                \ *-\ *
                (?P<day_to>\d+)\.\ *(?P<month_to>\d+)\.\ *(?P<year_from>\d+)
                \ *$''', # 1. 9.  - 3. 11. 2013
            r'''^\ *
                (?P<day_from>\d+)\.
                \ *-\ *
                (?P<day_to>\d+)\.\ *(?P<month_from>\d+)\.\ *(?P<year_from>\d+)
                \ *$''', # 7.  - 8. 9. 2013
        ]
        for pattern in patterns:
            found = re.match(pattern, raw, re.VERBOSE)
            if found:
                d = found.groupdict()
                print d
                year_from = int(d['year_from'])
                month_from = int(d['month_from'])
                day_from = int(d['day_from'])
                year_to = 'year_to' in d and int(d['year_to']) or year_from
                month_to = 'month_to' in d and int(d['month_to']) or month_from
                day_to = 'day_to' in d and int(d['day_to']) or day_from
                time_from = None
                time_to = None
                if 'hour_from' in d and 'minute_from' in d:
                    time_from = time(int(d['hour_from']), int(d['minute_from']))
                if 'hour_to' in d and 'minute_to' in d:
                    time_to = time(int(d['hour_to']), int(d['minute_to']))
                return date(year_from, month_from, day_from), date(year_to, month_to, day_to), time_from, time_to
        print repr(raw)
        raise ValueError(repr(raw))
        return None, None, None, None


