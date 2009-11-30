def template(template_name):
	def renderer(func):
		def wrapper(request, *args, **kw):
			context_dict = func(request, *args, **kw)
			if not isinstance(context_dict, dict):
				return context_dict
			from django.template import RequestContext, loader
			from django.http import HttpResponse
			context = RequestContext(request, context_dict)
			template = loader.get_template(template_name)
			return HttpResponse(template.render(context))
		return wrapper
	return renderer
