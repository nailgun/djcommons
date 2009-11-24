var DeliverySelect2 = function(element, callbackUrl, initial, chainField) {
    DeliverySelect2.super.call(this, element, callbackUrl, initial, chainField);

	this.costSpan = $(this.element).nextAll('span')[0];
}

DeliverySelect2.extends(ChainedSelect);

DeliverySelect2.prototype.updateCost = function(option) {
	var cost = option.data[2];
	if(cost) {
		this.costSpan.innerHTML = cost;
	} else {
		this.costSpan.innerHTML = '';
	}
}

DeliverySelect2.prototype.changed = function(value, option) {
    DeliverySelect2.super.prototype.changed.call(this, value, option);
    this.updateCost(option)
}
