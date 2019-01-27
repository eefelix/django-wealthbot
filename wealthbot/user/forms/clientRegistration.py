from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User

class ClientRegistrationForm(UserCreationForm):
	first_name = forms.CharField(max_length=255, required=True,
		widget=forms.TextInput(
			attrs={
			    'placeholder': 'First Name',
			    'class': 'width-150 form-control',
			}
		)
	)
	last_name = forms.CharField(max_length=255,
		widget=forms.TextInput(
			attrs={
			    'placeholder': 'Last Name',
			    'class': 'width-150 form-control',
			}
		)
	)
	email = forms.EmailField(required=True,
		widget=forms.EmailInput(
			attrs={
			    'placeholder': 'Your Email',
			    'class': 'form-control',
			}
		)
	)
	is_accepted = forms.BooleanField(required=True,
		widget=forms.CheckboxInput(
			attrs={
				'required': 'required',
				'class': 'pull-left',
				'value': '1',
			}
		)
	)

	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			'is_accepted',
		)

	def __init__(self, *args, **kwargs):
		super(ClientRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['password1'].widget = forms.PasswordInput(
			attrs={
			    'placeholder': 'Create Password',
			    'class': 'form-control',
			}
		)
		self.fields['password2'].widget = forms.PasswordInput(
			attrs={
			    'placeholder': 'Verify Password',
			    'class': 'form-control',
			}
		)

	def save(self, commit=True):
		user = super(ClientRegistrationForm, self).save(commit=False)

		if commit:
			user.save()
			user.setRoles(['ROLE_CLIENT'])

		return user
