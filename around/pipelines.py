from datetime import date, time, datetime

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
        data = {
            "date_from": item['date_from'],
            "date_to": item['date_to'],
            "name": item['name'],
            "venue": item['venue'],
            "source": item['source'],
            "link": item['link'],
            "coords": {
                'lat': item['coords_lat'],
                'lon': item['coords_lon'],
            }
        }
        for field in ('time_from', 'time_to', 'description'):
            if item[field]:
                data[field] = item[field]
                if isinstance(data[field], time):
                    data[field] = data[field].strftime("%H:%M:%S")

        self.client.index(
            "around",
            "event",
            data,
            id='%s-%s' % (item['source'], item['id']),
        )
        return data

