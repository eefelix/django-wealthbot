from datetime import datetime
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from client.forms import PortfolioForm
from client.models import ClientAccount, AccountGroup
from client.managers.clientPortfolioManager import ClientPortfolioManager
from client.managers.portfolioInformationManager import PortfolioInformationManager

@login_required
def index(request):
	clientPortfolioManager = ClientPortfolioManager()

	# Get the user object
	client = request.user
	ria = client.profile.ria_user
	
	# Get client's portfolio
	clientPortfolio = clientPortfolioManager.getCurrentPortfolio(client=client)

	if clientPortfolio is None:
		clientPortfolio = clientPortfolioManager.getActivePortfolio(client=client)

	if clientPortfolio is None:
		raise Http404()

	companyInformation = ria.riacompanyinformation
	portfolio = clientPortfolio.portfolio
	isQualified = manageQualified(
		session=request.session,
		companyInformation=companyInformation,
		isQualified=request.GET.get('is_qualified')
	)
	isFinal = False

	# If client has final portfolio
	if clientPortfolio.isAdvisorApproved():
		isFinal = True
		if client.profile.registration_step < 4:
			profile = client.profile
			profile.registration_step = 4
			profile.save()
	elif clientPortfolio.isProposed():
		existWorkflow = None # Skip implementing workflow at this moment

	portfolioInformationManager = PortfolioInformationManager()
	clientAccounts = ClientAccount.objects.filter(client=client)
	retirementAccounts = ClientAccount.objects.filter(client=client, groupType__group__name=AccountGroup.GROUP_EMPLOYER_RETIREMENT)
	form = PortfolioForm()

	# Skip document at this moment
	documents = {
		'ria_investment_management_agreement': '#',
	}

	portfolio_information = portfolioInformationManager.getPortfolioInformation(user=client, model=portfolio, isQualified=isQualified)
	client.appointedBillingSpec.calcFeeTier()
	
	data = {
		'is_final': isFinal,
		'client': client,
		'client_accounts': clientAccounts,
		'total': ClientAccount.getTotalScoreByClient(client=client),
		'ria_company_information': companyInformation,
		'has_retirement_account': True if retirementAccounts.exists() else False,
		'portfolio_information': portfolio_information,
		'show_sas_cash': containsSasCash(clientAccounts),
		'is_use_qualified_models': companyInformation.is_use_qualified_models,
		'form': form,
		'signing_date': datetime.now(),
		'documents': documents,
		'action': 'client_portfolio',
	}

	return render(request, 'client/portfolio_index.html', data)

@login_required
def acceptPortfolio(request):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def consolidatedAccounts(request):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def outsideFunds(request):
	return HttpResponse('Not implemented yet, please come back later!')
	
# Returns true if array contains ClientAccount objects with sas cache property value
# more than 0 and false otherwise.
def containsSasCash(accounts=None):
	if accounts is not None:
		for account in accounts:
			if account.sas_cash is not None:
				if account.sas_cash > 0:
					return True

	return False

# Set what type of models RIA will be used (qualified or non-qualified).
def setIsQualifiedModel(session, value):
	session['portfolio_is_qualified'] = (value == '1')

# Get what type of models RIA will be used (qualified or non-qualified).
def getIsQualifiedModel(session):
	return (session['portfolio_is_qualified'] == True)

# Manage qualified parameters.
def manageQualified(session, companyInformation, isQualified):
	isUseQualified = companyInformation.is_use_qualified_models
	if isUseQualified:
		if isQualified != '':
			setIsQualifiedModel(session=session, value=isQualified)
		isQualified = getIsQualifiedModel(session=session)
	else:
		isQualified = False

	return isQualified
