from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django import forms
from django.db.models import Q
from django.contrib.auth.models import Group
from user.models import Profile, GroupOwner
from admin.models import CeModel, BillingSpec

class SuggestedPortfolioForm(forms.ModelForm):
	action_type = forms.CharField(widget=forms.HiddenInput(), required=False)
	unconsolidated_ids = forms.CharField(widget=forms.HiddenInput(), required=False)
	is_qualified = forms.CharField(widget=forms.HiddenInput(), required=False)
	prefix = 'suggested_portfolio_form'
	clientPortfolio = None
	choices = []
	client_portfolio = forms.ChoiceField(
		choices=choices,
	)
	groupChoices = []
	groups = forms.ChoiceField(
		choices=groupChoices,
	)
	billingSpecChoices = []
	billingSpec = forms.ChoiceField(
		choices=billingSpecChoices,
	)

	class Meta:
		model = Profile
		fields = (
			'client_portfolio',
			'groups',
			'billingSpec',
			'action_type',
			'unconsolidated_ids',
			'is_qualified',
			'paymentMethod',
			'client_account_managed',
		)

	def buildRetirementForm(self, riaCompanyInfo, client):
		clientPortfolios = client.clientportfolio_set.all()

		if (clientPortfolios.count() == 1):
			if clientPortfolios[0].isProposed():
				if riaCompanyInfo.isClientByClientManagedLevel():
					# print("riaCompanyInfo isClientByClientManagedLevel")
					pass
				else:
					self.initial['client_account_managed'] = riaCompanyInfo.account_managed
					self.fields['client_account_managed'].widget = forms.HiddenInput()
			else:
				self.fields['client_account_managed'].widget.attrs = {
					'disabled': True,
				}

		self.fields['client_account_managed'].widget.attrs['class'] = 'form-control'

		for field_name in self.fields:
			field = self.fields.get(field_name)
			if field and isinstance(field , forms.TypedChoiceField):
				field.choices = field.choices[1:]

		return

	def buildModelForm(self, ria):
		# Build the ChooseClientPortfolioForm in here instead of a separate Form class
		choices = []
		portfolio_models = CeModel.objects.filter(Q(owner=ria) & ~Q(parent=None))
		for portfolio_model in portfolio_models:
			choice = (portfolio_model.pk, portfolio_model.name)
			choices.append(choice)

		self.fields['client_portfolio'] = forms.ChoiceField(
			choices=choices,
		)
		self.fields['client_portfolio'].widget.attrs = {
		    'class': 'form-control',
		}
		self.initial['client_portfolio'] = self.clientPortfolio.portfolio.pk

		if ria.riacompanyinformation.isCollaborativeProcessing():
			groupChoices = []
			groupowner = GroupOwner.objects.filter(ria_user=ria)
			groups = Group.objects.filter(
				Q(groupowner__in=groupowner) |
				Q(groupowner=None)
			)
			for group in groups:
				groupChoice = (group.pk, group.name)
				groupChoices.append(groupChoice)

			self.fields['groups'] = forms.ChoiceField(
				choices=groupChoices
			)
			self.fields['groups'].widget.attrs = {
		    	'class': 'form-control',
			}

	def buildBillingSpecForm(self, client):
		ria = client.profile.ria_user
		billingSpecChoices = []
		billing_specs = BillingSpec.objects.filter(owner=ria)
		for billing_spec in billing_specs:
			billingSpecChoice = (billing_spec.pk, billing_spec.name)
			billingSpecChoices.append(billingSpecChoice)

		self.fields['billingSpec'] = forms.ChoiceField(
			choices=billingSpecChoices,
		)
		self.fields['billingSpec'].widget.attrs = {
		    'class': 'form-control',
		}
		self.initial['billingSpec'] = client.appointedBillingSpec.pk


	def __init__(self, *args, **kwargs):
		self.clientPortfolio = kwargs.pop('clientPortfolio')
		super(SuggestedPortfolioForm, self).__init__(*args, **kwargs)
		profile = self.instance
		ria = profile.ria_user
		client = profile.user
		riaCompanyInfo = ria.riacompanyinformation

		if profile is None:
			raise Http404("Profile is required.")

		self.buildRetirementForm(riaCompanyInfo=riaCompanyInfo, client=client)

		self.buildModelForm(ria=ria)

		self.buildBillingSpecForm(client=client)

		self.fields['paymentMethod'].widget.attrs['class'] = 'form-control'

		# Skip implementing the preferred fund check for retirement accounts at this moment

