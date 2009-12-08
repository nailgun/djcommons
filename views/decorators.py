import shortcuts

def template(template_name):
	def renderer(func):
		def wrapper(request, *args, **kwargs):
			context_dict = func(request, *args, **kwargs)
			if not isinstance(context_dict, dict):
				return context_dict
			return shortcuts.render_to_response(request, template_name,
					context_dict)
		return wrapper
	return renderer
