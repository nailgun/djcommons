from django import forms

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
