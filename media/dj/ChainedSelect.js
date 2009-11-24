var ChainedSelect = function(element, callbackUrl, initial, chainField) {
	ChainedSelect.super.call(this, element);

	this.callbackUrl = callbackUrl;
	this.chainField = chainField;

	if(initial) {
		this.element.value = initial;

		var t = this;
		$.get(callbackUrl, {pk: initial}, function(data) {
			var opt = document.createElement('option');
			ChainedSelect.Item.prototype.fillOption(opt, data[0]);
			$(t.element).after(
				'<span> ' + opt.text + ' <a href="#">change</a></span>'
			);

			t.changed(initial, opt);

			$(t.element).next('span').children('a').click(function(e) {
				e.preventDefault();
				$(this).parent().remove();
				t.element.value = null;
				var select = t.addSelect(t.element);
				t.changed(select.value, select.options[0]);
			});

		}, 'json');
	} else {
		this.addSelect(this.element);
	}
};

ChainedSelect.extends(Widget);

ChainedSelect.prototype.addSelect = function(after, parentItem) {
	var $after = $(after);
	$after.after(
		'<select style="display: none">'+
		'	<option value="">-----</option>'+
		'</select>'
	);

	var $select = $after.next('select');
	var select = $select[0];
	select.options[0].data = {};
	
	this.createItem(select, parentItem);

	var t = this;
	$(select).change(function() {
		$(this).nextAll('select').remove();

		var value;
		if(this.value) {
			value = this.value;
			t.addSelect(this, this);
		} else if(this.parentItem){
			value = this.parentItem.value;
		} else {
			value = this.value;
		}

		t.element.value = value;
		t.changed(value, this.options[this.selectedIndex]);
	});

	return select;
}

ChainedSelect.prototype.createItem = function(element, parentItem) {
	return new ChainedSelect.Item(element, this.callbackUrl,
			parentItem, this.chainField);
};

ChainedSelect.prototype.changed = function(value, option) {
};

ChainedSelect.Item = function(element, callbackUrl, parentItem, chainField) {
	this.parentItem = parentItem;
	this.chainField = chainField;
	ChainedSelect.Item.super.call(this, element, callbackUrl);
}

ChainedSelect.Item.extends(AjaxSelect);

ChainedSelect.Item.prototype.buildRequest = function() {
	var request = {};

	if(this.parentItem && this.parentItem.value) {
		request[this.chainField] = this.parentItem.value;
	} else {
		request[this.chainField] = '__none__';
	}

	return request;
}

ChainedSelect.Item.prototype.loadComplete = function() {
	ChainedSelect.Item.super.prototype.loadComplete.call(this);
	if(this.element.options.length > 1) {
		this.element.style.display = 'inline';
	}
}
