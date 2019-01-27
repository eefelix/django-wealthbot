import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from user.models import User

def logo(request, ria_id):
	# Check if the ria_id exists in users table or not
	ria = get_object_or_404(User, pk=ria_id)
	# Set the default logo path
	LogoPath = os.path.join(settings.BASE_DIR, 'static', 'img/logo.png')
	# Set Individual RIA company logo if it exists
	companyInformation = ria.riacompanyinformation
	if companyInformation is not None:
		if companyInformation.logo is not None:
			LogoPath = os.path.join(settings.UPLOAD_DIR, 'ria_company_logos', 
				companyInformation.logo)
	return FileResponse(open(LogoPath, 'rb'))
