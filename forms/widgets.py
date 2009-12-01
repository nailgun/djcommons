from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.forms import util
from django import forms
from djcommons import settings

def render_js_call(proc, *args):
	params = [simplejson.dumps(a) for a in args]
	params = ', '.join(params)
	call = "%s(%s);" % (proc, params)
	call = call.replace('</script>', '\\<\\/script\\>')
	return util.mark_safe('<script type="text/javascript">%s</script>' % call)

def media_from_definition(cls, base=None):
	if base is None:
		base = forms.Media()
		for base_cls in cls.__bases__:
			base += media_from_definition(base_cls)

	definition = getattr(cls, 'Media', None)
	if definition:
		extend = getattr(definition, 'extend', True)
		if extend:
			if extend == True:
				m = base
			else:
				m = forms.Media()
				for medium in extend:
					m += base[medium]
		else:
			m = forms.Media()

		use = getattr(definition, 'use', None)
		if use:
			for use_cls in use:
				m += media_from_definition(use_cls)

		return m + forms.Media(definition)
	else:
		return base

def media_property(cls):
	def _media(self):
		if hasattr(super(cls, self), 'media'):
			base = super(cls, self).media
		else:
			base = forms.Media()
		return media_from_definition(cls, base)
	return property(_media)

class MediaDefiningClass(forms.MediaDefiningClass):
	def __new__(cls, name, bases, attrs):
		new_class = type.__new__(cls, name, bases, attrs)

		if 'media' not in attrs:
			new_class.media = media_property(new_class)
		return new_class

class ActionWidget:
	__metaclass__ = MediaDefiningClass

	class Media:
		js = (settings.dj_media('Widget.js'), )

	def __init__(self, id):
		self.id = id

	def js_init(self, *args):
		return render_js_call('new ' + self.__class__.__name__, *args)

	def render_html(self):
		raise NotImplementedError

	def render_js(self):
		return self.js_init(self.id)

	def __unicode__(self):
		return self.render_html() + self.render_js()

class JSWidget(forms.Widget):
	__metaclass__ = MediaDefiningClass

	class Media:
		js = (settings.dj_media('Widget.js'), )

	def js_init(self, *args):
		return render_js_call('new ' + self.__class__.__name__, *args)

	def render_html(self, name, value, attrs=None):
		raise NotImplementedError

	def render_js(self, name, value, attrs):
		return self.js_init(attrs['id'])

	def render(self, name, value, attrs=None):
		return (self.render_html(name, value, attrs) +
				self.render_js(name, value, attrs))

class AjaxSelect(JSWidget):
	class Media:
		js = (
			settings.js_media('jquery.js'),
			settings.dj_media('AjaxSelect.js'),
		)

	def __init__(self, callback, attrs=None):
		self.callback = callback
		super(AjaxSelect, self).__init__(attrs)
	
	def render_html(self, name, value, attrs=None):
		return forms.Select(self.attrs).render(name, value, attrs)

	def render_js(self, name, value, attrs):
		return self.js_init(attrs['id'], reverse(self.callback), value)

class ChainedSelect(JSWidget):
	class Media:
		use = (AjaxSelect, )
		js = (settings.dj_media('ChainedSelect.js'), )

	def __init__(self, callback, chain_field, attrs=None):
		self.callback = callback
		self.chain_field = chain_field
		super(ChainedSelect, self).__init__(attrs)
	
	def render_html(self, name, value, attrs=None):
		return forms.HiddenInput(self.attrs).render(name, value, attrs)

	def render_js(self, name, value, attrs):
		return self.js_init(attrs['id'], reverse(self.callback),
				value, self.chain_field)

class KeypadWidget(JSWidget):
	class Media:
		js = (
			settings.js_media('jquery.js'),
			settings.dj_media('KeypadWidget.js'),
		)

	def __init__(self, letters, attrs=None):
		self.letters = letters
		super(KeypadWidget, self).__init__(attrs)
	
	def render_html(self, name, value, attrs=None):
		final_attrs = self.build_attrs(attrs)
		html = util.mark_safe('<span%s >' % util.flatatt(final_attrs))
		html += forms.TextInput().render(name, value)
		for ch in self.letters:
			html += util.mark_safe(
					'<input type="button" value="%s" />' %
					ch)
		html += util.mark_safe(
				'<input type="button" value="<-" />')
		html += '</span>'
		return html

# vim:set ft=python ts=4 sw=4 tw=79 noet: 
