
class RiskTolerance(object):
	user = None
	userAnswers = []
	points = None

	def __init__(self, user, userAnswers):
		self.user = user
		self.userAnswers = userAnswers
		self.points = None

	# Get answers points
	def getPoints(self):
		if self.points is None:
			self.calculatePoints()

		return self.points

	# Returns suggested portfolio.
	def getSuggestedPortfolio(self, allowedModels):
		result = None
		models = []
		points = self.getPoints()

		for model in allowedModels:
			rating = model.risk_rating

			if points == rating:
				return model

			if points > rating:
				models.append(model)

		if not models:
			models = allowedModels

		# Get the model with risk rating closet to the point
		tmpDiff = None
		ratingDiff = None

		for model in models:
			rating = model.risk_rating

			tmpDiff = abs(points - rating)

			if result is None:
				ratingDiff = tmpDiff
				result = model
			else:
				if tmpDiff < ratingDiff:
					ratingDiff = tmpDiff
					result = model

		return result		


	# Recalculate answers points
	def calculatePoints(self):
		points = 50

		for userAnswer in self.userAnswers:
			points += userAnswer.answer.point

		# map the points to correct the scale problem in original wealthbot code
		if points < 41:
			points = 1
		elif points < 50:
			points = 2
		elif points < 59:
			points = 3
		else:
			points = 4

		self.points = points

	# Get ria
	def getRia(self):
		if self.user.hasRole('ROLE_CLIENT'):
			return self.user.profile.ria_user

		return self.user
