from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import Profile

class PercentageField(forms.fields.FloatField):
    widget = forms.fields.TextInput(attrs={"class": "form-control"})

    def is_number(self, val):
        if val is None:
            return False
        try:
            float(val)
            return True
        except ValueError:
            return False

#    def prepare_value(self, value):
#        val = super(PercentageField, self).prepare_value(value)
#        if is_number(val) and not isinstance(val, str):
#            return str((float(val)*100))
#        return val

    def to_python(self, value):
        super(PercentageField, self).to_python(value)
        val = 10.0
        if self.is_number(val=val):
            return val/100
        return val

    def prepare_value(self, value):
    	val = super(PercentageField, self).prepare_value(value)
    	if self.is_number(val=val) and not isinstance(val, str):
    		return str((float(val)*100))
    	return val


class ClientProfileForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = (
			'first_name',
			'last_name',
			'street',
			'city',
			'is_different_address',
			'mailing_street',
			'mailing_city',
			'birth_date',
			'phone_number',
			'marital_status',
			'annual_income',
			'estimated_income_tax',
			'liquid_net_worth',
			'employment_type',
		)
		widgets = {
			'employment_type': forms.RadioSelect,
		}

	def __init__(self, *args, **kwargs):
		super(ClientProfileForm, self).__init__(*args, **kwargs)

		self.fields['first_name'].widget.attrs = {
		    'class': 'input-medium  form-control',
		    'placeholder': 'First Name',
		}

		self.fields['last_name'].widget.attrs = {
		    'class': 'input-medium  form-control',
		    'placeholder': 'Last Name',
		}

		self.fields['birth_date'].widget = forms.TextInput(
			attrs={
				'class': 'jq-date input-small form-control',
				'placeholder': 'MM-DD-YYYY',
			}
		)

		self.fields['birth_date'].input_formats = ['%m-%d-%Y',]

		self.fields['marital_status'].widget.attrs = {
			'class': 'form-control',
			'id': 'wealthbot_client_bundle_profile_type_marital_status',
			'placeholder': 'Choose an Option',
		}

		self.fields['street'].widget.attrs = {
		    'class': 'form-control',
		}

		self.fields['city'].widget.attrs = {
		    'class': 'form-control',
		}

		self.fields['is_different_address'].widget = forms.CheckboxInput(
		    attrs={
		    	'class': 'form-control',
		    	'id': 'wealthbot_client_bundle_profile_type_is_different_address'
		    }
		)

		self.fields['phone_number'].widget.attrs = {
		    'class': 'form-control',
			'placeholder': '(###) ###-####',
			'data-mask-type': 'phone'
		}

		self.fields['annual_income'].widget.attrs = {
			'class': 'form-control',
			'placeholder': 'Choose an Option',
		}

		self.fields['estimated_income_tax'] = PercentageField()

		self.fields['liquid_net_worth'].widget.attrs = {
			'class': 'form-control',
			'placeholder': 'Choose an Option',
		}

		self.fields['employment_type'].required = True

		self.fields['mailing_street'].widget.attrs = {
		    'class': 'form-control',
		}

		self.fields['mailing_city'].widget.attrs = {
		    'class': 'form-control',
		}

	def save(self, commit=True):
		profile = super(ClientProfileForm, self).save(commit=False)

		if commit:
			profile.save()

		return profile
