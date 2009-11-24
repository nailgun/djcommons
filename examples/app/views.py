from django.shortcuts import render_to_response
import forms

def widgets_example(request):
	if request.method == 'POST':
		form = forms.WidgetForm(request.POST)
		initial = request.POST
	else:
		form = forms.WidgetForm()
		initial = None

	return render_to_response('widgets.html', {
		'form': form,
		'initial': initial,
	})
