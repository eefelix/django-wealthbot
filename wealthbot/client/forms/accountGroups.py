from django import forms
from client.models import AccountGroup

class AccountGroupsForm(forms.Form):
	client = None
	prefix = 'client_account_types'

	def __init__(self, *args, **kwargs):
		self.client = kwargs.pop('user')
		super(AccountGroupsForm, self).__init__(*args, **kwargs)

		# Get the corresponding RIA company information
		riaCompanyInformation = self.client.profile.ria_user.riacompanyinformation
		# Get the choices of account groups
		choices = AccountGroup.getGroupChoices()

		# Remove retirement plan if the RIA firm not allow such plan
		if not riaCompanyInformation.is_allow_retirement_plan:
			del_choice = None
			for choice in choices:
				if choice[0] == AccountGroup.GROUP_EMPLOYER_RETIREMENT:
					del_choice = choice
			if del_choice is not None:
				choices.remove(del_choice)

		self.fields['groups'] = forms.ChoiceField(
			choices=choices,
			widget=forms.RadioSelect(
			)
		)
				