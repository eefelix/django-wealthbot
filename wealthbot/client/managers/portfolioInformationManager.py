from admin.models import SecurityAssignment
from admin.managers.feeManager import FeeManager
from client.managers.portfolioInformation import PortfolioInformation

class PortfolioInformationManager(object):
	feeManager = None

	def __init__(self):
		self.feeManager = FeeManager()

	def getPortfolioInformation(self, user, model, isQualified=False):
		if user.hasRole('ROLE_CLIENT'):
			ria = user.profile.ria_user
		else:
			ria = user

		portfolioInformation = PortfolioInformation()
		portfolioInformation.setUser(user=user)
		portfolioInformation.setModel(model=model)
		portfolioInformation.setIsQualifiedModel(isQualified=isQualified)
		portfolioInformation.setFees(fees=self.feeManager.getClientFees(ria))

		if model.owner.hasRole('ROLE_RIA'):
			transactionCommissionFees = SecurityAssignment.findMinAndMaxTransactionFeeForModel(model=model.parent)
			portfolioInformation.setTransactionCommissionFees(transactionCommissionFees=[transactionCommissionFees['minimum'], transactionCommissionFees['maximum']])

		return portfolioInformation
