from django.core.urlresolvers import reverse
from django import forms
from djcommons import forms as djforms

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
			widget=djforms.AjaxSelect('ajax-delivery-query'))
	custom_ajax_select = forms.CharField(
			widget=DeliverySelect('ajax-delivery-query'))
	chained_select = forms.CharField(
			widget=djforms.ChainedSelect('ajax-region-query', 'parent'))
	custom_chained_select = forms.CharField(
			widget=DeliverySelect2('ajax-region-query', 'parent'))
