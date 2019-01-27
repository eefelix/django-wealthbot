from django.db import models

class SecurityAssignment(models.Model):
    class Meta:
    	db_table = 'securities_assignments'
    security = models.ForeignKey('webo_admin.Security', on_delete=models.CASCADE, related_name='securityAssignments')
    subclass = models.ForeignKey('webo_admin.Subclass', on_delete=models.CASCADE, related_name='securityAssignments', blank=True, null=True)
    model = models.ForeignKey('webo_admin.CeModel', on_delete=models.CASCADE, blank=True, null=True)
    is_preferred = models.BooleanField()
    muni_substitution = models.BooleanField()

    def __str__(self):
    	return str(self.pk) + ": " + self.security.symbol

    def getExpenseRatio(self):
        if self.security is not None:
            return self.security.expense_ratio
        else:
            return 0

    @classmethod
    def findMinAndMaxTransactionFeeForModel(cls, model):
    	# Skip implementing transaction fee at this moment
        minAndMax = []
        minAndMax.append(0)
        minAndMax.append(11)
        return minAndMax
