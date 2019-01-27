from client.models import ClientPortfolio

class ClientPortfolioManager(object):

	# Propose portfolio for client.
	def proposePortfolio(self, client, portfolio):
		try:
			proposedPortfolio = ClientPortfolio.objects.get(
				client=client, 
				status=ClientPortfolio.STATUS_PROPOSED
			)
		except ClientPortfolio.DoesNotExist:
			proposedPortfolio = ClientPortfolio(
				client=client, 
				portfolio=portfolio, 
				is_active=True,
				status=ClientPortfolio.STATUS_PROPOSED,
			)

		proposedPortfolio.portfolio = portfolio

		proposedPortfolio.save()
		client.save()

		return proposedPortfolio
		
	# Find client current portfolio.
	def getCurrentPortfolio(self, client):
		try:
			currentPortfolio = ClientPortfolio.objects.get(
				client=client, 
				is_active=True, 
				status=ClientPortfolio.STATUS_CLIENT_ACCEPTED
			)
		except ClientPortfolio.DoesNotExist:
			currentPortfolio = None

		return currentPortfolio

	# Find client active portfolio.
	def getActivePortfolio(self, client):
		try:
			activePortfolio = ClientPortfolio.objects.get(
				client=client, 
				is_active=True, 
			)
		except ClientPortfolio.DoesNotExist:
			activePortfolio = None

		return activePortfolio
