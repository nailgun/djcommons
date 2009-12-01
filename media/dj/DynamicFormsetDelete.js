var DynamicFormsetDelete = function(element, formIdPrefix) {
	DynamicFormsetDelete.super.call(this, element);

	this.formIdPrefix = formIdPrefix;
	this.btn = $(this.element).next('input')[0];

	if(this.element.value) {
		$('#'+this.formIdPrefix).hide();
	}

	var t = this;
	$(this.btn).click(function() {
		t.element.value = '1';
		$('#'+t.formIdPrefix).hide();
	});
}

DynamicFormsetDelete.extends(Widget);

// vim:set ft=javascript ts=4 sw=4 tw=80 noet: 
