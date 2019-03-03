from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def accountManagement(request):
	return HttpResponse('Not implemented yet, please come back later!')	