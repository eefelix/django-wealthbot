from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django import forms
from client.models import ClientAccount
from client.models import AccountGroup, AccountGroupType

class RiaClientAccountForm(forms.ModelForm):
	groupChoices = [
		(AccountGroup.GROUP_DEPOSIT_MONEY, 'New Account'),
        (AccountGroup.GROUP_FINANCIAL_INSTITUTION, 'Transfer'),
        (AccountGroup.GROUP_OLD_EMPLOYER_RETIREMENT, 'Rollover'),		
	]

	group = forms.ChoiceField(
		choices=groupChoices,
	)
	consolidate = forms.BooleanField(
		required=False,
		widget=forms.CheckboxInput()
	)
	# unconsolidated_ids = forms.CharField(widget=forms.HiddenInput(), required=False)
	# is_qualified = forms.CharField(widget=forms.HiddenInput(), required=False)
	prefix = 'ria_client_account'
	client = None
	isAllowRetirementPlan = None
	validateAdditionalFields = None

	class Meta:
		model = ClientAccount
		fields = (
			'group',
			'groupType',
			'consolidate',
			'value',
			'monthly_contributions',
			'monthly_distributions',
			'sas_cash',
		)

	def __init__(self, *args, **kwargs):
		self.client = kwargs.pop('client')
		if 'validateAdditionalFields' in kwargs:
			self.validateAdditionalFields = kwargs.pop('validateAdditionalFields')
		else:
			self.validateAdditionalFields = True
		super(RiaClientAccountForm, self).__init__(*args, **kwargs)

		riaCompanyInformation = self.client.profile.ria_user.riacompanyinformation
		self.isAllowRetirementPlan = riaCompanyInformation.is_allow_retirement_plan

		# data (not self.data) is the model data
		data = self.instance

		# self.data (not data) is the pre-submit form filled data
		if self.data:
			# Prepopulated form being submit
			selectedGroup = data.getGroupName()
			consolidate = True if ((data.getConsolidatorId() is not None) or
				(not data.getUnconsolidated)) else False
			# Implement preBind and bind handlers here
		else:
			# New form being prepopulated
			selectedGroup = None
			consolidate = True
			# Implement preSetData event handler here
			if data.pk is not None:
				group = data.getGroupName()
				financialInstitution = data.financial_institution
				groupType = data.groupType
			else:
				group = None
				financialInstitution = None
				groupType = None

			self.updateFieldsByGroup(group=group, financialInstitution=financialInstitution)



		self.fields['group'].initial = selectedGroup

		if consolidate:
			self.fields['consolidate'].widget.attrs = { 'checked': 'checked' }
		else:
			self.fields['consolidate'].widget.attrs = {}

		self.fields['value'].label = 'Estimated Value'

		self.fields['monthly_contributions'].label = 'Estimated Monthly Contributions'
		self.fields['monthly_contributions'].required = False

		self.fields['monthly_distributions'].label = 'Estimated Monthly Distributions'
		self.fields['monthly_distributions'].required = False

		self.fields['sas_cash'].required = False

    # Update form fields by group.
	def updateFieldsByGroup(self, group, financialInstitution=None):
		# Skip implementing those fields update relating to financial_institution at this moment
		# default case
		group = AccountGroup.GROUP_DEPOSIT_MONEY
		self.updateGroupTypeField(group=group)

    # Update groupType field by group.
	def updateGroupTypeField(self, group):
		# Get the list of tuple of account types corresponding to the group
		choices = [('', 'Select Type')]
		groupObj = AccountGroup.objects.get(name=group)
		types = AccountGroupType.objects.filter(group=groupObj)
		for type in types:
			choice = (type.type.name, type.type.name)
			choices.append(choice)

		self.fields['groupType'] = forms.ChoiceField(
			choices=choices,
		)
		self.fields['groupType'].label = 'Account Type'
		self.fields['groupType'].widget.attrs = {
		    'class': 'form-control',
		}
