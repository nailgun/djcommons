from djcommons import ajax
import models

def region_format(region):
    return (region.pk, region.name, region.pk*3, bool(region.pk%2))

def delivery_format(region):
    return (region.pk, unicode(region), region.pk*3, bool(region.pk%2))

region_query = ajax.query_all(models.Region, region_format).callback
delivery_query = ajax.query_all(models.Region, delivery_format).callback
