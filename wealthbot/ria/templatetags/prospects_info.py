from django import template
from django.template.loader import render_to_string
from user.models import User

register = template.Library()

@register.filter
def prospectsInformation(ria):
	clientsData = User.findOrderedProspectsByRia(ria)

	context = {
		'clients_data': clientsData,
	}

	return render_to_string('ria/prospects_index.html', context)
