from django.db import models

class SecurityTransaction(models.Model):
    class Meta:
    	db_table = 'security_transaction'
    security_assignment = models.OneToOneField('webo_admin.SecurityAssignment', on_delete=models.CASCADE, related_name='securityTransaction')
    transaction_fee = models.FloatField(blank=True, null=True)
    transaction_fee_percent = models.FloatField(blank=True, null=True)
    minimum_buy = models.FloatField(blank=True, null=True)
    minimum_initial_buy = models.FloatField(blank=True, null=True)
    minimum_sell = models.FloatField(blank=True, null=True)
    redemption_penalty_interval = models.IntegerField(blank=True, null=True)
    redemption_fee = models.FloatField(blank=True, null=True)
    redemption_percent = models.FloatField(blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.security_assignment.security.symbol
    