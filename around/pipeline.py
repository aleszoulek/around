class FillCoords(object):
    coords = {
        u'Z\xe1mek Dob\u0159ichovice - Dob\u0159ichovice': (1,2),
        u'Lumen - domek Jeka - Palack\xe9ho 147, Dob\u0159ichovice': (20, 30),
    }
    def process_item(self, item, spider):
        if item['venue'] in self.coords:
            item['coords_lat'], item['coords_long'] = self.coords[item['venue']]
        return item
