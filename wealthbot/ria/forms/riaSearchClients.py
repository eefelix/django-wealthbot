from django import forms

class RiaSearchClientsForm(forms.Form):

	prefix = 'wealthbot_riabundle_ria_find_clients_form_type'

	def __init__(self, *args, **kwargs):
		super(RiaSearchClientsForm, self).__init__(*args, **kwargs)

		self.fields['search'] = forms.CharField(required=False)
				