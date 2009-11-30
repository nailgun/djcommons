from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.forms import util
from django import forms
import settings

def render_js_call(proc, *args):
	params = [simplejson.dumps(a) for a in args]
	params = ', '.join(params)
	return util.mark_safe('<script type="text/javascript">' +
			"%s(%s);" % (proc, params) +
			'</script>')

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

class BinaryNumberField(forms.Field):
	default_error_messages = {
		'invalid': u'Enter binary number.',
		'max_value': u'Ensure this value is less than or equal to %d',
		'min_value': u'Ensure this value is greater than or equal to %d',
		'max_digits': u'Ensure that there are no more digits than %d.',
		'min_digits': u'Ensure that there are no less digits than %d.',
	}

	def __init__(self, max_value=None, min_value=None, max_digits=None,
			min_digits=None, **kwargs):
		self.max_value, self.min_value = max_value, min_value
		self.max_digits, self.min_digits = max_digits, min_digits
		super(BinaryNumberField, self).__init__(**kwargs)

	def clean(self, value):
		value = super(BinaryNumberField, self).clean(value)
		if not value:
			return None
		value = smart_str(value).strip()

		if self.max_digits is not None and len(value) > self.max_digits:
			raise forms.ValidationError(self.error_messages['max_digits'] %
					self.max_digits)

		if self.min_digits is not None and len(value) < self.min_digits:
			raise forms.ValidationError(self.error_messages['min_digits'] %
					self.min_digits)

		try:
			value = int(value, 2)
		except ValueError:
			raise forms.ValidationError(self.error_messages['invalid'])

		if self.max_value is not None and value > self.max_value:
			raise forms.ValidationError(self.error_messages['max_value'] %
					self.max_value)

		if self.min_value is not None and value < self.min_value:
			raise forms.ValidationError(self.error_messages['min_value'] %
					self.min_value)

		return value

class GetOrCreateModelField(forms.Field):
	def __init__(self, manager, lookup_field, ignore_case=False, **kwargs):
		self.manager = manager
		self.lookup_field = lookup_field
		self.ignore_case = ignore_case
		field = manager.model._meta.get_field_by_name(lookup_field)[0]
		self.wrapped = field.formfield(**kwargs)
		self.widget = self.wrapped.widget
		super(GetOrCreateModelField, self).__init__(**kwargs)
	
	def clean(self, value):
		value = self.wrapped.clean(value)
		lookup = self.lookup_field
		if self.ignore_case:
			lookup += '__iexact'
		filter = { lookup: value }
		try:
			obj = self.manager.get(**filter)
		except self.manager.model.DoesNotExist:
			obj = self.manager.create(**{ self.lookup_field: value })
		return obj

# vim:set ft=python ts=4 sw=4 tw=79 noet: 
