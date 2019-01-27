from client.models import ClientQuestionnaireAnswer, RiskAnswer
from client.managers.riskTolerance import RiskTolerance
from admin.managers.ceModelManager import CeModelManager

class RiskToleranceManager(object):
	user = None
	userAnswers = []
	riskTolerance = None

	def __init__(self, user, answers):
		self.user = user
		self.userAnswers = self.createUserAnswers(answers)
		self.riskTolerance = RiskTolerance(user=user, userAnswers=self.userAnswers)

	# Save userAnswers in db
	def saveUserAnswers(self):
		for userAnswer in self.userAnswers:
			userAnswer.save()

	# Returns suggested portfolio.
	def getSuggestedPortfolio(self):
		modelManager = CeModelManager()
		ria = self.riskTolerance.getRia()
		parentModel = ria.riacompanyinformation.portfolio_model

		return self.riskTolerance.getSuggestedPortfolio(modelManager.getChildModels(parentModel))

	# Create and return array of ClientQuestionnaireAnswer objects by answers array
	def createUserAnswers(self, answers):
		userAnswers = []

		for answer in answers:

			# Get corresponding question and answer objects
			question = answer['question']
			data = answer['data']

			if question.is_withdraw_age_input:
				data = self.getAnswerForWithdrawAgeQuestion(question, answer['data'])

			userAnswer = ClientQuestionnaireAnswer(client=self.user, question=question, 
				answer=data)

			userAnswers.append(userAnswer)

		return userAnswers

	# Return RiskAnswer object for withdraw age input question
	def getAnswerForWithdrawAgeQuestion(self, question, ageDiff):
		answers = RiskAnswer.objects.filter(risk_question=question.pk).order_by('title').reverse()

		result = None

		for answer in answers:
			string = answer.title
			symbol = string[:1]
			number = int(string[1:])

			if symbol == '>':
				if ageDiff >= number:
					return answer
			else:
				if ageDiff <= number:
					result = answer

		return result
