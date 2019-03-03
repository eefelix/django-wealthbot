from django import template
from django.template.loader import render_to_string
from ria.forms import RiaSearchClientsForm

register = template.Library()

@register.filter
def companyInformation(ria):
	riaCompanyInformation = ria.riacompanyinformation

	progress = 0
	# Skip implementing model completion at this moment
	modelCompletion = None

	form = None
	searchForm = RiaSearchClientsForm()


	context = {
		'company_information': riaCompanyInformation,
		'form': form,
		'progress': progress,
		'searchForm': searchForm,
	}

	return render_to_string('ria/dashboard_company_information.html', context)
