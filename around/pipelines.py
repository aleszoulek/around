from elasticsearch import Elasticsearch



class FillCoords(object):
    coords = {
        u'Z\xe1mek Dob\u0159ichovice - Dob\u0159ichovice': (1,2),
        u'Lumen - domek Jeka - Palack\xe9ho 147, Dob\u0159ichovice': (20, 30),
        u'kostel Karl\xedk - Karl\xedk': (50,60),
    }
    def process_item(self, item, spider):
        if item['venue'] in self.coords:
            item['coords_lat'], item['coords_long'] = self.coords[item['venue']]
        return item


class ElasticSearchSave(object):
    client = Elasticsearch()


    def process_item(self, item, spider):
        self.client.index(
            "around",
            "event",
            {
                "name": item['name'],
                "venue": item['venue'],
                "source": item['source'],
                "description": item['description'],
                "link": item['link'],
                "coords": (item['coords_long'], item['coords_lat']),
            },
            id='%s-%s' % (item['source'], item['id']),
        )

