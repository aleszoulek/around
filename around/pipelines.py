from elasticsearch import Elasticsearch



class FillCoords(object):
    coords = {
        u'Z\xe1mek Dob\u0159ichovice - Dob\u0159ichovice': (49.9262642, 14.2748719),
        u'Lumen - domek Jeka - Palack\xe9ho 147, Dob\u0159ichovice': (49.9267081, 14.2750847),
        u'kostel Karl\xedk - Karl\xedk': (49.9356092, 14.2613125),
    }
    def process_item(self, item, spider):
        if item['venue'] in self.coords:
            item['coords_lat'], item['coords_lon'] = self.coords[item['venue']]
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
                "coords": {
                    'lat': item['coords_lat'],
                    'lon': item['coords_lon'],
                },
            },
            id='%s-%s' % (item['source'], item['id']),
        )
        return item

