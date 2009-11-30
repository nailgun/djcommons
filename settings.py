from django.conf import settings

DJ_URL = getattr(settings, 'DJ_URL', 'dj/')
JS_PREFIX = getattr(settings, 'JS_PREFIX', 'js/')
CSS_PREFIX = getattr(settings, 'CSS_PREFIX', 'css/')

def dj_media(filename):
	return '%s/%s' % (DJ_URL, filename)

def js_media(filename):
	return '%s/%s' % (JS_PREFIX, filename)

def css_media(filename):
	return '%s/%s' % (CSS_PREFIX, filename)
