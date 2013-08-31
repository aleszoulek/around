# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class EventItem(Item):
    name = Field()
    venue = Field()
    source = Field()
    description = Field()
    link = Field()
    id = Field()
    coords_lat = Field()
    coords_lon = Field()
