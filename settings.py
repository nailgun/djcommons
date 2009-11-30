from django.conf import settings

DJ_URL = getattr(settings, 'DJ_URL', 'dj/')
JS_PREFIX = getattr(settings, 'JS_PREFIX', 'js/')
CSS_PREFIX = getattr(settings, 'CSS_PREFIX', 'css/')

def dj_media(filename):
	return ''.join((DJ_URL, filename))

def js_media(filename):
	return ''.join((JS_PREFIX, filename))

def css_media(filename):
	return ''.join((CSS_PREFIX, filename))
