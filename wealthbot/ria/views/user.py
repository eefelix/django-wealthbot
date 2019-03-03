from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def userIndex(request):
	return HttpResponse('Not implemented yet, please come back later!')

