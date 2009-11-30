from django.utils import simplejson
from django import http

def clean_query_value(value):
	mapping = {
		'__true__': True,
		'__false__': False,
		'__none__': None,
	}
	return mapping.get(value, value)

def default_pack(obj):
	return (obj.pk, unicode(obj))

def object_list(request, queryset, pack_func=default_pack):
	raw_data = [pack_func(i) for i in queryset]
	data = simplejson.dumps(raw_data)
	return http.HttpResponse(data, content_type='application/json')

def object_query(request, queryset, pack_func=default_pack, filter_args=None):
	lookup = {}

	if filter_args:
		for k,v in request.GET.items():
			k = str(k)
			try:
				k = filter_args[k]
			except KeyError:
				pass
			else:
				lookup[k] = clean_query_value(v)
	else:
		for k,v in request.GET.items():
			lookup[str(k)] = clean_query_value(v)

	result_set = queryset.filter(**lookup)
	raw_data = [pack_func(i) for i in result_set]
	data = simplejson.dumps(raw_data)
	return http.HttpResponse(data, content_type='application/json')
