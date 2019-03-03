from django import template
from django.urls import resolve
from django.template.loader import render_to_string

register = template.Library()

@register.filter
def dashboardMenu(ria, arg):
	route = resolve(arg).url_name
	riaCompanyInformation = ria.riacompanyinformation

	context = {
		'route': route,
		'riaCompanyInformation': riaCompanyInformation,
	}

	return render_to_string('ria/dashboard_menu.html', context)
