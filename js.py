from django.utils import simplejson
from django.utils.safestring import mark_safe

def render_call(proc, *args):
	params = [simplejson.dumps(a) for a in args]
	params = ', '.join(params)
	return mark_safe('<script type="text/javascript">' +
			"%s(%s);" % (proc, params) +
			'</script>')

def widget_init(self, *args):
	return render_call('new ' + self.__class__.__name__, *args)
