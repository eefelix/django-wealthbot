from django.db import models
from user.models import User

class RiskQuestion(models.Model):
    class Meta:
    	db_table = 'risk_questions'
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_withdraw_age_input = models.BooleanField()
    sequence = models.IntegerField()

    def __str__(self):
    	return str(self.pk) + ": " + self.title

    def getOwnerQuestionsOrAdminIfNotExists(self, ownerId, order='asc'):
        questions = self.getOrderedQuestionsByOwnerId(ownerId, order)
        if not questions:
            return self.getAdminQuestions(order)

        return questions

    def getOrderedQuestionsByOwnerId(self, ownerId, order='asc'):
        if order == 'asc':
            return RiskQuestion.objects.filter(owner_id=ownerId).order_by('sequence')
        else:
            return RiskQuestion.objects.filter(owner_id=ownerId).order_by('sequence').reverse()

    def getAdminQuestions(self, order='asc'):
        # Owner ID must be '1' for Admin
        if order == 'asc':
            return RiskQuestion.objects.filter(owner_id=1).order_by('sequence')
        else:
            return RiskQuestion.objects.filter(owner_id=1).order_by('sequence').reverse()
