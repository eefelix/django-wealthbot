from django import forms
from ria.models import RiskQuestion
from client.models import ClientQuestionnaireAnswer

class RiskQuestionsForm(forms.Form):
	user = None
	questions = RiskQuestion.objects.none()

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(RiskQuestionsForm, self).__init__(*args, **kwargs)

		# Get the corresponding RIA
		riaId = self.user.profile.ria_user.pk
		riskQuestion = RiskQuestion()
		self.questions = riskQuestion.getOwnerQuestionsOrAdminIfNotExists(ownerId=riaId)

		# Iterlate the question queryset
		for question in self.questions:
			if question.is_withdraw_age_input:
				self.fields['client_birth_date'] = forms.DateField()
				self.fields['answer_{}'.format(question.pk)] = forms.CharField(
					label=question.title,
					initial=self.user.profile.withdraw_age
				)
			else:
				# Get user answer if replied previously
				userAnswer = ClientQuestionnaireAnswer.objects.filter(
					client_id=self.user.pk,
					question_id=question.pk
				).first()

				placeholder = 'Choose an Option'
				if userAnswer is not None:
					userAnswer = userAnswer.answer # Get the RiskAnswer object
					placeholder = False

				# Enumerate all answers to form the choices of the question
				answers = [('', 'Choose an Option'),]
				for answer in question.riskanswer_set.all(): 
					answers.append((answer.pk, answer.title))

				# Create the question field
				self.fields['answer_{}'.format(question.pk)] = forms.ChoiceField(
					label=question.title,
					choices=[answers],
					initial=userAnswer,
				)
				self.fields['answer_{}'.format(question.pk)].widget.attrs = {
					'placeholder': placeholder,
					'class': 'control-label',
				}
