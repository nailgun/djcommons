from django.utils.translation import ugettext as _
from django.forms import formsets
from django.forms import util
from django import forms
from djcommons import settings
from django.template import Context, loader
import widgets

class DynamicFormsetAdd(widgets.ActionWidget):
	class Media:
		js = (
			settings.js_media('jquery.js'),
			settings.dj_media('DynamicFormsetAdd.js'),
		)

	def __init__(self, id, formset_id_prefix, new_form_template):
		self.formset_id_prefix = formset_id_prefix
		self.new_form_template = new_form_template
		super(DynamicFormsetAdd, self).__init__(id)
	
	def render_js(self):
		return self.js_init(self.id, self.formset_id_prefix,
				self.new_form_template)

	def render_html(self):
		return util.mark_safe(u'<input type="button" id="%s" value="Add" />' %
				self.id)

class DynamicFormsetDelete(widgets.JSWidget):
	class Media:
		js = (
			settings.js_media('jquery.js'),
			settings.dj_media('DynamicFormsetDelete.js'),
		)

	def __init__(self, form_id_prefix, attrs=None):
		self.form_id_prefix = form_id_prefix
		super(DynamicFormsetDelete, self).__init__(attrs)
	
	def render_js(self, name, value, attrs):
		return self.js_init(attrs['id'], self.form_id_prefix)

	def render_html(self, name, value, attrs=None):
		return forms.HiddenInput(self.attrs).render(name, value, attrs) + \
			util.mark_safe(u'<input type="button" value="Delete" />')

def dynamic_formset(form_template, formset):
	def get_id(auto_id, name):
		if auto_id and '%s' in auto_id:
			return auto_id % name
		elif auto_id:
			return name
		else:
			return ''

	def add_fields(self, form, index):
		self.add_fields_wrapped(form, index)
		form.id_prefix = get_id(form.auto_id, form.prefix)

		if self.can_delete:
			form.fields[formsets.DELETION_FIELD_NAME] = \
				forms.BooleanField(
					label=_(u'Delete'), required=False,
					widget=DynamicFormsetDelete(form.id_prefix))
		form.empty_permitted = False

	formset.add_fields_wrapped = formset.add_fields
	formset.add_fields = add_fields

	# from django/forms/models.py
	def pk_is_not_editable(pk):
		return ((not pk.editable) or (pk.auto_created or
				isinstance(pk, AutoField)) or (pk.rel and pk.rel.parent_link
					and pk_is_not_editable(pk.rel.to._meta.pk)))

	def formset_init(self, *args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)

		self.new_form = self.form(
			auto_id=self.auto_id,
			prefix=self.add_prefix('%INDEX%')
		)
		self.add_fields(self.new_form, 0)
		if hasattr(self, 'model'):
			pk = self.model._meta.pk
			if pk_is_not_editable(pk):
				del self.new_form.fields[pk.name]

		t = loader.get_template(form_template)
		c = Context({'form': self.new_form})
		new_form_template = t.render(c)

		self.id_prefix = get_id(self.auto_id, self.prefix)
		add_id = get_id(self.auto_id, self.add_prefix('ADD'))
		self.form_add = DynamicFormsetAdd(add_id, self.id_prefix,
				new_form_template)
		self.null_form_id = get_id(self.auto_id, self.add_prefix('NULL'))

	formset.__init__ = formset_init

	def _media(self):
		return self.media_wrapped + self.form_add.media + self.new_form.media

	formset.media_wrapped = formset.media
	formset.media = property(_media)

	return formset
