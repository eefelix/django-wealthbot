from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def workflowIndex(request, tab='active'):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def deleteActivitySummary(request, id):
	return HttpResponse('Not implemented yet, please come back later!')
