from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def account(request):
	pass
	
