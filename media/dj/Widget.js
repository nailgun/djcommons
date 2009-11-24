Function.prototype.extends = function(super) {
	var Inheritance = function(){};
	Inheritance.prototype = super.prototype;

	this.prototype = new Inheritance();
	this.prototype.constructor = this;
	this.super = super;
}

var Widget = function(element) {
	if(typeof element == 'string') {
		this.element = this.byId(element);
		this.element.widget = this;
	} else {
		this.element = element;
		element.widget = this;
	}
};

Widget.prototype.byId = function(id) {
	return document.getElementById(id);
}
