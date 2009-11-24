var KeypadWidget = function(element) {
	KeypadWidget.super.call(this, element);

	this.lcd = $(this.element).children('input[type=text]')[0];

	var t = this;
	$(this.element).children('input[type=button]').click(function() {
		if(this.value == '<-') {
			t.back();
		} else {
			t.enter(this.value);
		}
	});
};

KeypadWidget.extends(Widget);

KeypadWidget.prototype.enter = function(letter) {
	this.lcd.value = this.lcd.value + letter;
};

KeypadWidget.prototype.back = function() {
	this.lcd.value = this.lcd.value.slice(0, this.lcd.value.length - 1);
};

// vim:set ft=javascript ts=4 sw=4 tw=80 noet: 
