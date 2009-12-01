var DynamicFormsetAdd = function(element, formsetIdPrefix, newFormTemplate) {
	DynamicFormsetAdd.super.call(this, element);

	this.formsetIdPrefix = formsetIdPrefix;
	this.newFormTemplate = newFormTemplate;

	var t = this;
	$(this.element).click(function() {
		var totalForms = t.byId(t.formsetIdPrefix + '-TOTAL_FORMS')
		var lastForm;
		if(totalForms.value != 0) {
			lastForm = t.byId(t.formsetIdPrefix + '-' +
				(totalForms.value-1));
		} else {
			lastForm = t.byId(t.formsetIdPrefix + '-NULL');
		}
		var newFormHtml = 
			t.newFormTemplate.split('%INDEX%').join(totalForms.value);
		$(lastForm).after(newFormHtml);
		totalForms.value++;
	});
}

DynamicFormsetAdd.extends(Widget);

// vim:set ft=javascript ts=4 sw=4 tw=80 noet: 
