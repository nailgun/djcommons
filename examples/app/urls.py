from django.conf.urls.defaults import *

from django.views.generic import simple
import views
import ajax

urlpatterns = patterns('',
	(r'^$', simple.direct_to_template, {'template': 'index.html'}),
	(r'widgets/$', views.widgets_example),

	(r'ajax/regions/$', ajax.region_query),
	(r'ajax/delivery/$', ajax.delivery_query),
)
