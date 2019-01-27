from django import template
from django.template.loader import render_to_string
from client.models import ClientAccount

register = template.Library()

@register.filter
def showAccountsTable(client):
	total = ClientAccount.getTotalScoreByClient(client=client)

	context = {
		'client': client,
		'total': total,
		'show_action_btn': True,
	}

	return render_to_string('client/profile_accounts_list.html', context)
