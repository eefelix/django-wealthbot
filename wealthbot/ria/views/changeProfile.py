from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def changeProfileIndex(request, tab='company_profile'):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def profile(request, tab='profile'):
	return HttpResponse('Not implemented yet, please come back later!')
	