from django import forms
from user.models import User

# Skip implementing InviteProspectForm at this moment
class InviteProspectForm(forms.ModelForm):
	type = forms.CharField(max_length=255, required=True,
		widget=forms.TextInput(
			attrs={
			    'placeholder': 'First Name',
			    'class': 'width-150 form-control',
			}
		)
	)

	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'email',
			'groups',
			'type',
		)

	ria = None

	def __init__(self, *args, **kwargs):
		self.ria = kwargs.pop('ria')
		super(InviteProspectForm, self).__init__(*args, **kwargs)

		# Get the corresponding RIA
		riaId = self.ria.pk

