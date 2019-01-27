from django import forms
from ria.models import RiskQuestion
from client.models import ClientQuestionnaireAnswer
from ria.forms import RiskQuestionsForm

class ClientQuestionsForm(RiskQuestionsForm):
	user = None
	questions = RiskQuestion.objects.none()

	def __init__(self, *args, **kwargs):
		super(ClientQuestionsForm, self).__init__(*args, **kwargs)

		# Iterlate the question queryset
		for question in self.questions:
			if question.is_withdraw_age_input:
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
					choices=answers,
					initial=userAnswer,
				)
				self.fields['answer_{}'.format(question.pk)].widget.attrs = {
					'placeholder': placeholder,
					'class': 'form-control',
				}
				