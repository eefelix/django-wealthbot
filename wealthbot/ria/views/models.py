from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def modelsIndex(request, withLayout=True):
	return HttpResponse('Not implemented yet, please come back later!')

