import json
from django.forms.models import model_to_dict

class PortfolioInformation(object):
	user = None
	model = None
	assumption = None
	fees = None
	isQualified = None
	modelEntitiesJson = None
	transactionCommissionFee = None
	isShowPerformanceSection = None

	def __init__(self):
		self.assumption = None
		self.fees = []
		self.isQualified = False
		self.modelEntitiesJson = {}
		self.transactionCommissionFee = []
		self.isShowPerformanceSection = False

	# Set user
	def setUser(self, user):
		self.user = user

		return self

	def getUser(self):
		return self.user

	# Set model
	def setModel(self, model):
		self.model = model
		self.model.buildGroupModelEntities()

		return self
	
	# Get model.
	def getModel(self):
		return self.model

	# Set qualified flag
	def setIsQualifiedModel(self, isQualified):
		self.isQualified = isQualified

		return self

	# Get qualified flag
	def getIsQualifiedModel(self):
		self.isQualified

	# Set fees
	def setFees(self, fees=[]):
		self.fees = fees

		return self

	# Get fees
	def getFees(self):
		return self.fees

	# Set transaction commission fees
	def setTransactionCommissionFees(self, transactionCommissionFees):
		self.transactionCommissionFee = transactionCommissionFees

	# Get transaction commission fees
	def getTransactionCommissionFees(self):
		return self.transactionCommissionFee

	# Get model entities called by template
	def modelEntities(self):
		if self.isQualified:
			return self.model.getQualifiedModelEntities()

		return self.model.getNonQualifiedModelEntities()

	# Get model entities information as json called by template
	def modelEntitiesAsJson(self):
		if self.modelEntitiesJson:
			# If self.modelEntitiesJson is not empty
			return self.modelEntitiesJson

		data = []

		for entity in self.modelEntities():
			data.append(entity.toArray())

		self.modelEntitiesJson = json.dumps(data)

		return self.modelEntitiesJson
	
	# Get fund expenses
	def fundExpenses(self):
		expenses = 0

		for entity in self.modelEntities():
			percent = entity.percent
			expenseRatio = entity.security_assignment.getExpenseRatio()

			expenses += percent * expenseRatio / 100

		return expenses

	# Get investment market.
	def investmentMarket(self):
		investment = 0

		for entity in self.modelEntities():
			percent = entity.percent
			expectedPerformance = entity.subclass.expected_performance
			investment += percent * expectedPerformance / 100

		return investment

	# Get commissions as string.
	def commissionsAsString(self):
		commissions = []

		if self.model.owner.hasRole('ROLE_RIA'):
			commissions = self.getTransactionCommissionFees()
		elif self.model.owner.hasRole('ROLE_CLIENT'):
			commissions = self.model.getCommissions()

		print(commissions)
		resultStr = None
		if commissions:
			resultStr = '$' + "{:.2f}".format(commissions[0]) + ' - ' + '$' + "{:.2f}".format(commissions[1])

		return resultStr

	def generousInvestmentMarket(self):
		generousMarketReturn = self.model.generous_market_return
		if generousMarketReturn is not None:
			gim = self.investmentMarket() * generousMarketReturn
		else:
			gim = self.investmentMarket() * 1.2

		return gim

	def averageInvestmentMarket(self):
		return self.investmentMarket() * 1

	def lowInvestmentMarket(self):
		lowMarketReturn = self.model.low_market_return
		if lowMarketReturn is not None:
			lim = self.investmentMarket() * lowMarketReturn
		else:
			lim = self.investmentMarket() * 0.8

		return lim

