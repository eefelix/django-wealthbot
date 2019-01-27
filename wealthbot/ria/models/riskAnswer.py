from django.db import models
from ria.models import RiskQuestion

class RiskAnswer(models.Model):
    class Meta:
    	db_table = 'risk_answers'
    risk_question = models.ForeignKey(RiskQuestion, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    point = models.IntegerField()

    def __str__(self):
    	return str(self.pk) + ": " + self.title
