from django import forms
from client.models import ClientAdditionalContact

class ClientSpouseForm(forms.ModelForm):

	class Meta:
		model = ClientAdditionalContact
		fields = (
			'first_name',
			'last_name',
			'birth_date',
		)

	def __init__(self, *args, **kwargs):
		super(ClientSpouseForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].widget.attrs = {
		    'class': 'input-medium  form-control',
		    'placeholder': 'First Name',
		}

		self.fields['last_name'].widget.attrs = {
		    'class': 'input-medium  form-control',
		    'placeholder': 'Last Name',
		}

		self.fields['birth_date'].input_formats = ['%m-%d-%Y',]

		self.fields['birth_date'].widget = forms.TextInput(
			attrs={
				'class': 'jq-date input-small form-control',
				'placeholder': 'MM-DD-YYYY',
			}
		)

	def save(self, commit=True):
		spouse = super(ClientSpouseForm, self).save(commit=False)
		spouse.type = ClientAdditionalContact.TYPE_SPOUSE

		if commit:
			spouse.save()

		return spouse
