import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from client.models import Activity, Workflow
from user.models import User
from ria.forms import RiaSearchClientsForm, InviteProspectForm

# Create your views here.
@login_required
def index(request):
	# Get the ria user object
	user = request.user
	clients = User.findClientsByRia(ria=user)

	recentActivity = Activity.objects.filter(ria_user=user, is_show_ria=True).order_by('created_at').reverse()
	recentActivityPagination = Paginator(recentActivity, 10).get_page(1)

	if request.is_ajax() and request.GET.get('block') == 'most_recent_activity':
		# Skip implementing ajax call at this moment
		data = {
			'status': 'success',
		}
		return JsonResponse(data)

	# Skip implementing riaDashboardBoxes at this moment
	blocksSequence = []

	prospects = User.findOrderedProspectsByRia(user)
	notApprovedPortfolios = User.findClientsWithNotApprovedPortfolioByRia(user)

	# Skip implementing workflow initial rebalance count at this moment
	portfoliosCount = {
		'prospects': len(prospects),
		'suggested_portfolios': notApprovedPortfolios.count(),
		'initial_rebalance': 0,
	}

	securitiesStatistic = [
        {'label': 'Vanguard Total Stock Market', 'data': 50000000},
        {'label': 'iShares Total Bond', 'data': 40000000},
        {'label': 'DFA Large Cap Value', 'data': 20000000},
        {'label': 'American Funds Growth Fund', 'data': 10000000},
        {'label': 'Vanguard Intermediate Bond', 'data': 10000000},
	]

	context = {
        'user': user,
        'clients': clients,
        'company_information': user.riacompanyinformation,
        'blocks_sequence': json.dumps(blocksSequence),
        'paperwork_counts': Workflow.getPaperworkCountsByRia(riaId=user),
        'portfolios_counts': portfoliosCount,
        'securities_statistic': json.dumps(securitiesStatistic),
        'recent_activity_pagination': recentActivityPagination,
	}

	return render(request, 'ria/dashboard_index.html', context)

@login_required
def swapBoxes(request):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def clientsList(request, tab=None):
	# Get the ria user object
	ria = request.user

	if tab is not None:
		activeTab = tab
	else:
		activeTab = 'prospects'

	inviteForm = InviteProspectForm(ria=ria)

	context = {
		'ria': ria,
		'inviteForm': inviteForm,
		'activeTab': activeTab,
		'searchForm': RiaSearchClientsForm(),
	}

	return render(request, 'ria/dashboard_clients_list.html', context)

@login_required
def securities(request, tab):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def rebalancing(request):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def clientsSearchWithProspects(request):
	return clientsSearch(request=request, with_prospects=1)

@login_required
def clientsSearch(request, with_prospects=0):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def showClient(request, client_id):
	return HttpResponse('Not implemented yet, please come back later!')
