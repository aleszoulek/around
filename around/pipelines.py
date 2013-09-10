from datetime import date, time, datetime

from elasticsearch import Elasticsearch

from scrapy.exceptions import DropItem



class FillCoords(object):
    coords = {
        # Dobrichovice
        u'Z\xe1mek Dob\u0159ichovice - Dob\u0159ichovice': (49.9262642, 14.2748719),
        u'Lumen - domek Jeka - Palack\xe9ho 147, Dob\u0159ichovice': (49.9267081, 14.2750847),
        u'S\xe1l Dr. F\xfcrsta - Dob\u0159ichovice': (49.9258303, 14.2723569),
        u'Dob\u0159ichovice - Dob\u0159ichovice': (49.9270781, 14.2748739),
        u'iLumen - Dob\u0159ichovice': DropItem,
        # Karlik
        u'kostel Karl\xedk - Karl\xedk': (49.9356092, 14.2613125),
        u'Karl\xedk - Karl\xedk': (49.9361600, 14.2616664),
        # Lety
        u'N\xe1ves - Obec Lety': (49.9215817, 14.2555433),
        u'Restaurace MMX Lety - Dob\u0159ichovick\xe1 452, Lety': (49.9232783, 14.2585544),
        # Karlstejn
        u'Hrad Karl\u0161tejn - Karl\u0161tejn 172': (49.9393128, 14.1883561),
        u'Hrad Karl\u0161tejn - 26718': (49.9393128, 14.1883561),
        u'Karl\u0161tejn - Karl\u0161tejn': (49.9393128, 14.1883561),
        u'Ryt\xed\u0159sk\xfd s\xe1l hradu Karl\u0161tejn - 26718': (49.9393128, 14.1883561),
        u'Restaurace u B\xedl\xe9 pan\xed - Karl\u0161tejn 58': (49.9389731, 14.1894239),
        u'S\xe1l restaurace U JAN\u016e - Karl\u0161tejn, 26718': (49.9375847, 14.1864794),
        u'Hrad a m\u011bstys Karl\u0161tejn - 26718': (49.9366044, 14.1843464),
        u'Kon\xedrna C\xedsa\u0159sk\xe9ho pal\xe1ce - 26718': (49.9393128, 14.1883561),
        u'Ark\xe1dy C\xedsa\u0159sk\xe9ho pal\xe1ce - 26718': (49.9393128, 14.1883561),
        u'Karl\u0161tejn\u0161t\xed maz\xe1ci o.s. - Karl\u0161tejn': DropItem,
        u'Autokemp Karl\u0161tejn - Karl\u0161tejn': (49.9335019, 14.1692103),
        # Mnisek p/Brdy
        u'Skalka, barokn\xed are\xe1l - Mn\xed\u0161ek pod Brdy': (49.8776558, 14.2538461),
        u'Mn\xed\u0161ek pod Brdy - Mn\xed\u0161ek pod Brdy': (49.8664644, 14.2604750),
        u'Kostel sv. V\xe1clava - Mn\xed\u0161ek pod Brdy': (49.8664078, 14.2600861),
        u'St\xe1tn\xed z\xe1mek Mn\xed\u0161ek pod Brdy - Mn\xed\u0161ek pod Brdy': (49.8680689, 14.2581961),
        u'Z\xe1mek Mn\xed\u0161ek pod Brdy - N\xe1m\u011bst\xed F.X. Svobody 1, 252 10': (49.8680689, 14.2581961),
        # Vseradice
        u'Minigolfov\xe9 h\u0159i\u0161t\u011b - V\u0161eradice': (49.8730244, 14.1111008),
        u'Galerie Dobromila - V\u0161eradice 1': (49.8730244, 14.1111008),
        u'Z\xe1meck\xfd dv\u016fr V\u0161eradice - 267 26 V\u0161eradice 1': (49.8730244, 14.1111008),
        u'V\u0161eradice - V\u0161eradice': (49.8737244, 14.1050339),
        # Vsenory
        u'S\xe1l O\xda V\u0161enory - Obecn\xed \xfa\u0159ad V\u0161enory, U silnice 151': (49.9333700, 14.3080900),
        # Morinka
        u'obecn\xed \xfa\u0159ad Mo\u0159inka - Mo\u0159inka': (49.9385339, 14.2345317),
        # Zbraslav
        u'Restaurace Kam\xednka - Nad Kam\xednkou 1523, Praha Zbraslav': (49.9641281, 14.3884586),
        # Cernosice
        u'Club Kino - F\xfcgnerova 263, \u010cerno\u0161ice': (49.9589458, 14.3190989),
        
    }
    def process_item(self, item, spider):
        if item['venue'] in self.coords:
            coords = self.coords[item['venue']]
            if coords is DropItem:
                raise DropItem(item['venue'])
            item['coords_lat'], item['coords_lon'] = coords
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

