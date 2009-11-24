var AjaxSelect = function(element, callbackUrl, initial) {
	AjaxSelect.super.call(this, element);

	this.initial = initial;
	this.callbackUrl = callbackUrl;
	this.loadData();
};

AjaxSelect.extends(Widget);

AjaxSelect.prototype.handleItem = function(data) {
	var opt = document.createElement('option');
	this.fillOption(opt, data);
	this.element.add(opt);
};

AjaxSelect.prototype.fillOption = function(opt, data) {
	opt.value = data[0];
	opt.text = data[1];
	opt.data = data;
};

AjaxSelect.prototype.buildRequest = function() {
	return {};
};

AjaxSelect.prototype.loadData = function() {
	var obj = this;
	$.get(this.callbackUrl, this.buildRequest(), function(data) {
		for(var key in data) {
			obj.handleItem(data[key]);
		}

		obj.loadComplete()
	}, 'json');
};

AjaxSelect.prototype.loadComplete = function() {
	this.element.value = this.initial;
};

// vim:set ft=javascript ts=4 sw=4 tw=80 noet: 
