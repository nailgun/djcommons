var DeliverySelect = function(element, callbackUrl, initial) {
    DeliverySelect.super.call(this, element, callbackUrl, initial);

	this.costSpan = $(this.element).next('span')[0];

    var t = this;
    $(this.element).change(function() {
        t.updateCost();
    });
}

DeliverySelect.extends(AjaxSelect);

DeliverySelect.prototype.updateCost = function() {
    var opt = this.element.options[this.element.selectedIndex];
    this.costSpan.innerHTML = opt.data[2];
}

DeliverySelect.prototype.loadComplete = function() {
    DeliverySelect.super.prototype.loadComplete.call(this);
    this.updateCost()
}
