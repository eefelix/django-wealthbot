from django import forms
from client.forms import ClientAccountForm

class TypedClientAccountForm(ClientAccountForm):

	groupType = None

	def __init__(self, *args, **kwargs):
		self.groupType = kwargs.pop('groupType')

		super(TypedClientAccountForm, self).__init__(*args, **kwargs)

	def buildFormForFinancialInstitution(self):
		if self.groupType is not None:
			self.fields['groupType'].widget = forms.HiddenInput()
			self.fields['groupType'].initial = self.groupType.type.name
		else:
			group = self.group
			isAllowRetirementPlan = self.isAllowRetirementPlan
	
			# Get the list of tuple of account types corresponding to the group
			choices = [('', 'Select Type')]
			groupObj = AccountGroup.objects.get(name=self.group)
			types = AccountGroupType.objects.filter(group=groupObj)
			for type in types:
				choice = (type.type.name, type.type.name)
				choices.append(choice)
	
			self.fields['groupType'] = forms.ChoiceField(
				choices=choices,
			)
			self.fields['groupType'].label = 'Account Type:'
	
		self.fields['financial_institution'].label = 'Financial Institution:'
	
		self.fields['value'].label = 'Estimated Deposit:'

	def buildFormForDepositMoney(self):
		if self.groupType is not None:
			self.fields['groupType'].widget = forms.HiddenInput()
			self.fields['groupType'].initial = self.groupType.type.name
		else:
			group = self.group
			isAllowRetirementPlan = self.isAllowRetirementPlan

			# Get the list of tuple of account types corresponding to the group
			choices = [('', 'Select Type')]
			groupObj = AccountGroup.objects.get(name=self.group)
			types = AccountGroupType.objects.filter(group=groupObj)
			for type in types:
				choice = (type.type.name, type.type.name)
				choices.append(choice)

			self.fields['groupType'] = forms.ChoiceField(
				choices=choices,
			)
			self.fields['groupType'].label = 'Account Type:'

		del self.fields['financial_institution']

		self.fields['value'].label = 'Estimated Deposit:'

