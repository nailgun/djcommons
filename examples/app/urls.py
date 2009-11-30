from django.conf.urls.defaults import *
from django.views.generic import simple
from djcommons.views import json

import views
import models

def region_pack(region):
    return (region.pk, region.name, region.pk*3, bool(region.pk%2))

def delivery_pack(region):
    return (region.pk, unicode(region), region.pk*3, bool(region.pk%2))

urlpatterns = patterns('',
	(r'^$', simple.direct_to_template, {
		'template': 'index.html'
	}, 'index'),

	(r'widgets/$', views.widgets_example, {
	}, 'widgets-example'),

	(r'ajax/regions/$', json.object_query, {
		'queryset': models.Region.objects.all(),
		'pack_func': region_pack,
	}, 'ajax-region-query'),

	(r'ajax/delivery/$', json.object_query, {
		'queryset': models.Region.objects.all(),
		'pack_func': delivery_pack,
	}, 'ajax-delivery-query'),
)
