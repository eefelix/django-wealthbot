from django.db import models
from user.models import User
from ria.models import RiskQuestion, RiskAnswer

class ClientQuestionnaireAnswer(models.Model):
    class Meta:
    	db_table = 'client_questionnaire_answers'
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(RiskQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(RiskAnswer, on_delete=models.CASCADE)

    def __str__(self):
    	return str(self.pk) + ": " + self.client.username + " - " + self.answer.title
