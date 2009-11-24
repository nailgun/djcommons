from django import http
from django.utils import simplejson

def default_pack(obj):
	return (obj.pk, unicode(obj))

def clean_value(value):
	mapping = {
		'__true__': True,
		'__false__': False,
		'__none__': None,
	}
	return mapping.get(value, value)

class ModelQuery:
	def __init__(self, queryset, pack_func=default_pack):
		self.queryset = queryset
		self.pack_func = pack_func
	
	def callback(self, request):
		lookup = {}
		for k,v in request.GET.items():
			lookup[str(k)] = clean_value(v)
		result_set = self.queryset.filter(**lookup)
		raw_data = [self.pack_func(i) for i in result_set]
		data = simplejson.dumps(raw_data)
		return http.HttpResponse(data, content_type='application/json')

def query_all(model, pack_func=default_pack):
	return ModelQuery(model.objects.all(), pack_func)
