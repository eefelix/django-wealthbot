from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from client.managers.clientPortfolioManager import ClientPortfolioManager
from client.managers.portfolioInformationManager import PortfolioInformationManager
from user.models import User, Profile
from client.models import ClientQuestionnaireAnswer, ClientAccount
from ria.forms import SuggestedPortfolioForm, RiaClientAccountForm

# Create your views here.
@login_required
def createClientAccount(request, client_id):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def updateClientAccountForm(request, client_id):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def updateClientAccountOwnersForm(request, client_id):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def editClientAccount(request, client_id, account_id):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def deleteClientAccount(request, client_id, account_id):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def deleteProspect(request):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def inviteProspect(request):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def suggestedPortfolio(request, client_id, client_view=0):
	clientPortfolioManager = ClientPortfolioManager()
	# Get the ria and client objects
	ria = request.user
	client = get_object_or_404(User, pk=client_id)

	clientPortfolio = clientPortfolioManager.getActivePortfolio(client=client)

	if clientPortfolio is None:
		raise Http404("This client does not have suggested portfolio.")

	# Skip implementing mailer at this moment

	portfolio = clientPortfolio.portfolio


	if request.method == 'POST':
		settingsForm = SuggestedPortfolioForm(request.POST, instance=client.profile,
			clientPortfolio=clientPortfolio)
		if settingsForm.is_valid():
			portfolio = settingsForm.save(commit=False)
	else:
		settingsForm = SuggestedPortfolioForm(instance=client.profile,
			clientPortfolio=clientPortfolio)

	companyInformation = ria.riacompanyinformation
	isUseQualified = companyInformation.isUseQualifiedModels()
	isQualified = False

	if isUseQualified:
		# Skip implementing isQualified setting logic at this moment
		pass

	form = RiaClientAccountForm(client=client)

	clientAccounts = ClientAccount.findConsolidatedAccountsByClient(client=client)
	portfolioInformationManager = PortfolioInformationManager()
	portfolio_information = portfolioInformationManager.getPortfolioInformation(
		user=client,
		model=portfolio,
		isQualified=isQualified
	)
	client.appointedBillingSpec.calcFeeTier()

	if bool(client_view):
		parent_template = 'ria/clear_layout.html'
	else:
		parent_template = 'ria/dashboard_index.html'

	context = {
        'is_client_view': bool(client_view),
        'user': ria,
        'form': form,
        'total': ClientAccount.getTotalScoreByClient(client=client),
        'client': client,
        'client_accounts': clientAccounts,
        'settings_form': settingsForm,
        'client_answers': ClientQuestionnaireAnswer.objects.filter(client=client),
        'has_retirement_account': ClientAccount.hasRetirementAccount(client=client),
        'ria_company_information': ria.riacompanyinformation,
        'client_has_final_portfolio': clientPortfolio.isAdvisorApproved(),
        'portfolio_information': portfolio_information,
        'is_use_qualified_models': isUseQualified,
        'action': 'ria_suggested_portfolio',
        'billing_spec': client.appointedBillingSpec,
        'parent_template': parent_template,
	}

	return render(request, 'ria/prospects_suggested_portfolio.html', context)

@login_required
def prospectIndex(request):
	return HttpResponse('Not implemented yet, please come back later!')
