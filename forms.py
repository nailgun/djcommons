from django.core.urlresolvers import reverse
from django.forms import util
from django import forms
import js

class AjaxSelect(forms.Select):
	class Media:
		js = ('js/jquery.js', 'dj/Widget.js', 'dj/AjaxSelect.js', )

	def __init__(self, callback, attrs=None):
		self.callback = callback
		super(AjaxSelect, self).__init__(attrs)
	
	def render_html(self, name, value, attrs=None):
		return super(AjaxSelect, self).render(name, value, attrs)

	def render(self, name, value, attrs=None):
		return (self.render_html(name, value, attrs) +
				self.render_js(attrs['id'], reverse(self.callback), value))
	render_js = js.widget_init

class ChainedSelect(AjaxSelect):
	class Media:
		js = ('dj/ChainedSelect.js', )

	def __init__(self, callback, chain_field, attrs=None):
		self.callback = callback
		self.chain_field = chain_field
		super(ChainedSelect, self).__init__(callback, attrs)
	
	def render_html(self, name, value, attrs=None):
		return forms.HiddenInput(self.attrs).render(name, value, attrs)

	def render(self, name, value, attrs=None):
		return (self.render_html(name, value, attrs) +
				self.render_js(attrs['id'], reverse(self.callback), value,
					self.chain_field))

class KeypadWidget(forms.Widget):
	class Media:
		js = ('js/jquery.js', 'dj/Widget.js', 'dj/KeypadWidget.js', )

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

	def render(self, name, value, attrs=None):
		return (self.render_html(name, value, attrs) +
				self.render_js(attrs['id']))
	render_js = js.widget_init

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
