from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
	return render(request, 'user/default_index.html')

def switchToAdminAction(request):
    return redirect('rx_admin_homepage')
    