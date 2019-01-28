from django.db import models
from django.db.models import Max, Min
from admin.models import SecurityTransaction

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
    	# Get the set of security assignments for particular model
        security_assignments = SecurityAssignment.objects.filter(model=model)
        security_transactions = SecurityTransaction.objects.filter(security_assignment__in=security_assignments)
        minAndMax = {}
        minAndMax['minimum'] = security_transactions.aggregate(Min('transaction_fee')).get('transaction_fee__min')
        minAndMax['maximum'] = security_transactions.aggregate(Max('transaction_fee')).get('transaction_fee__max')

        if minAndMax['minimum'] is None:
            minAndMax['minimum'] = 0

        if minAndMax['maximum'] is None or minAndMax['maximum'] < minAndMax['minimum']:
            minAndMax['maximum'] = minAndMax['minimum']

        return minAndMax
