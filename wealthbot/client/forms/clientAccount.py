from django import forms
from client.models import ClientAccount, AccountGroup, AccountGroupType

class ClientAccountForm(forms.ModelForm):

	client = None
	group = None

	isAllowRetirementPlan = False
	contributionTypes = []

	contribution_type = forms.ChoiceField(
		choices=contributionTypes,
		widget=forms.RadioSelect(
		)
	)

	class Meta:
		model = ClientAccount
		fields = (
			'groupType',
			'financial_institution',
			'value',
			'monthly_contributions',
			'monthly_distributions',
			'contribution_type',
		)

	def __init__(self, *args, **kwargs):
		# print('1. Get into ClientAccountForm constructor')
		self.client = kwargs.pop('user')
		if 'group' in kwargs:
			self.group = kwargs.pop('group')
		else:
			self.group = AccountGroup.GROUP_EMPLOYER_RETIREMENT
		# print('1b. Group is %s' % self.group)
		self.isAllowRetirementPlan = self.client.profile.ria_user.riacompanyinformation.is_allow_retirement_plan
		if 'validateAdditionalFields' in kwargs:
			self.validateAdditionalFields = kwargs.pop('validateAdditionalFields')
		else:
			self.validateAdditionalFields = True
		# print('2. Construct contribution_type dict')
		self.contributionTypes = [
			('contributions', 'Contributions'),
			('distributions', 'Distributions'),
			('neither', 'Neither'),
		]
		# print('3. Call the parent modelform constructor')
		super(ClientAccountForm, self).__init__(*args, **kwargs)
		# print('4. Build different form depending on the account group')
		# Build the form depending on the account group
		if self.group == AccountGroup.GROUP_FINANCIAL_INSTITUTION:
			self.buildFormForFinancialInstitution()
		elif self.group == AccountGroup.GROUP_DEPOSIT_MONEY:
			self.buildFormForDepositMoney()
		elif self.group == AccountGroup.GROUP_OLD_EMPLOYER_RETIREMENT:
			self.buildFormForOldEmployerRetirement()
		elif self.group == AccountGroup.GROUP_EMPLOYER_RETIREMENT:
			self.buildFormForEmployerRetirement()
		else:
			self.buildFormForManually()

		contributionTypes = self.contributionTypes
		# print('5. Build the contribution_type form')
		if (self.group, self.group) in AccountGroup.getGroupChoices():
			# print('6. Valid account group')
			group = self.group

			data = self.instance
			# print('7. Data instance is')
			# print(data)
			# print('8. Form data have')
			# print(self.data)

			if self.data:
				# Prepopulated form being submit
				if 'contribution_type' in self.data:
					# print('From field contribution_type is %s' % self.data['contribution_type'])
					if self.data['contribution_type'] == "contributions":
						self.fields['monthly_contributions'].label = 'Estimated Monthly Contributions'
						del self.fields['monthly_distributions']
					elif self.data['contribution_type'] == "distributions":
						self.fields['monthly_distributions'].label = 'Estimated Monthly Distributions'
						del self.fields['monthly_contributions']
					else:
						del self.fields['monthly_contributions']
						del self.fields['monthly_distributions']
				else:
					if hasattr(data, 'monthly_contributions'):
						self.fields['monthly_contributions'].label = 'Estimated Monthly Contributions'
						self.fields['monthly_contributions'].initial = data.monthly_contributions
					elif hasattr(data, 'monthly_distributions'):
						self.fields['monthly_distributions'].label = 'Estimated Monthly Distributions'
						self.fields['monthly_distributions'].initial = data.monthly_distributions
				if 'contribution_type' in self.fields:
					del self.fields['contribution_type']
			else:
				# New form being prepopulated
				if (data is not None) and (data.pk is not None):
					# If the client has chosen the contribution type
					# print("Data instance exists with pk = %d" % data.pk)
					if data.monthly_contributions is not None:
						self.fields['monthly_contributions'].label = 'Estimated Monthly Contributions'
						self.fields['monthly_contributions'].initial = data.monthly_contributions
					elif data.monthly_distributions is not None:
						self.fields['monthly_distributions'].label = 'Estimated Monthly Distributions'
						self.fields['monthly_distributions'].initial = data.monthly_distributions
				else:
					# Else display the contribution type choices
					# print("Data instance or pk not exists")
					if group == AccountGroup.GROUP_EMPLOYER_RETIREMENT:
						# Do not allow withdrawal for retirement plan
						contributionTypes = [
							('contributions', 'Contributions'),
							('neither', 'None'),
						]
	
					self.fields['contribution_type'] = 	forms.ChoiceField(
						choices=contributionTypes,
						widget=forms.RadioSelect(
						)
					)

	def save(self, commit=True):
		clientAccount = super(ClientAccountForm, self).save(commit=False)
		#type = self.cleaned_data['groupType']
		#typeObj = AccountType.objects.get(name=type)
		#groupObj = AccountGroup.objects.get(name=self.group)
		#groupType = AccountGroupType.objects.get(group=groupObj, type=typeObj)
		#clientAccount.groupType = groupType
		
		if commit:
			clientAccount.save()

		return clientAccount

	def buildFormForFinancialInstitution(self):
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

		self.fields['value'].label = 'Estimated Value'

	def buildFormForDepositMoney(self):
		group = self.group
		isAllowRetirementPlan = self.isAllowRetirementPlan

		# Get the list of tuple of account types corresponding to the group
		choices = [('', 'Select Type')]
		groupObj = AccountGroup.objects.get(name=self.group)
		types = AccountGroupType.objects.filter(group=groupObj)
		for type in types:
			# print("Type Choice")
			# print(type.type.name)
			choice = (type.type.name, type.type.name)
			choices.append(choice)

		self.fields['groupType'] = forms.ChoiceField(
			choices=choices,
		)
		self.fields['groupType'].label = 'Account Type:'

		del self.fields['financial_institution']

		self.fields['value'].label = 'Estimated Value'

	def buildFormForOldEmployerRetirement(self):
		group = self.group
		isAllowRetirementPlan = self.isAllowRetirementPlan

		# Get the list of tuple of account types corresponding to the group
		choices = [('', 'Select Type')]
		groupObj = AccountGroup.objects.get(name=self.group)
		types = AccountGroupType.objects.filter(group=groupObj).order_by(type.pk).reverse()
		for type in types:
			choice = (type.type.name, type.type.name)
			choices.append(choice)

		self.fields['groupType'] = forms.ChoiceField(
			choices=choices,
		)
		self.fields['groupType'].label = 'Account Type:'

		self.fields['financial_institution'].label = 'Former Employer:'
		
		self.fields['value'].label = 'Estimated Value'

	def buildFormForEmployerRetirement(self):
		pass
