from django import forms
from client.models import AccountGroup, AccountGroupType

class AccountTypesForm(forms.Form):
	group = None
	client = None
	prefix = 'client_account_types'

	def __init__(self, *args, **kwargs):
		self.group = kwargs.pop('group')
		self.client = kwargs.pop('user')
		super(AccountTypesForm, self).__init__(*args, **kwargs)

		# Get the corresponding RIA company information
		riaCompanyInformation = self.client.profile.ria_user.riacompanyinformation
		# Get the property if the RIA firm allow retirement plan or not
		isAllowRetirementPlan = riaCompanyInformation.is_allow_retirement_plan

		# Get the list of tuple of account types corresponding to the group
		choices = []
		groupObj = AccountGroup.objects.get(name=self.group)
		types = AccountGroupType.objects.filter(group=groupObj)
		for type in types:
			choice = (type.type.name, type.type.name)
			choices.append(choice)

		self.fields['group_type'] = forms.ChoiceField(
			choices=choices,
			widget=forms.RadioSelect(
			)
		)
		self.fields['groups'] = forms.CharField(initial=self.group, widget=forms.HiddenInput())
				