from django.shortcuts import render_to_response as render_to_response_orig
from django.template import RequestContext

def render_to_response(request, *args, **kwargs):
	kwargs['context_instance'] = RequestContext(request)
	return render_to_response_orig(*args, **kwargs)
