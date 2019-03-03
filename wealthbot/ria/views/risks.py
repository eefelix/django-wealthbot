from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def riskIndex(request, withLayout=True):
	return HttpResponse('Not implemented yet, please come back later!')

@login_required
def testResult(request):
	return HttpResponse('Not implemented yet, please come back later!')

