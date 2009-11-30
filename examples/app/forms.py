from django.core.urlresolvers import reverse
from django import forms
from djcommons import forms as djforms
import ajax

class DeliverySelect(djforms.AjaxSelect):
	class Media:
		js = ('js/DeliverySelect.js', )
	
	def render_html(self, name, value, attrs=None):
		html = super(DeliverySelect, self).render_html(name, value, attrs)
		html += ' Delivery cost: <span></span>'
		return html

class DeliverySelect2(djforms.ChainedSelect):
	class Media:
		js = ('js/DeliverySelect2.js', )
	
	def render_html(self, name, value, attrs=None):
		html = super(DeliverySelect2, self).render_html(name, value, attrs)
		html += ' Delivery cost: <span></span>'
		return html

class WidgetForm(forms.Form):
	keypad = forms.CharField(widget=djforms.KeypadWidget('0123456789'))
	ajax_select = forms.CharField(
			widget=djforms.AjaxSelect(ajax.delivery_query))
	custom_ajax_select = forms.CharField(
			widget=DeliverySelect(ajax.delivery_query))
	chained_select = forms.CharField(
			widget=djforms.ChainedSelect(ajax.region_query, 'parent'))
	custom_chained_select = forms.CharField(
			widget=DeliverySelect2(ajax.region_query, 'parent'))
