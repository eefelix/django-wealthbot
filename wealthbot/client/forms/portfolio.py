from django import forms

class PortfolioForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(PortfolioForm, self).__init__(*args, **kwargs)

		self.fields['name'] = forms.CharField()
				