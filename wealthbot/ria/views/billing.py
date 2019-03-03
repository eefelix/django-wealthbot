from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def billingIndex(request):
	return HttpResponse('Not implemented yet, please come back later!')
