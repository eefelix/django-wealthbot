from django.db import models

class Fee(models.Model):
    class Meta:
    	db_table = 'fees'
    billing_spec = models.ForeignKey('webo_admin.BillingSpec', on_delete=models.CASCADE, related_name='fees')
    fee_with_retirement = models.FloatField(blank=True, null=True)
    fee_without_retirement = models.FloatField(blank=True, null=True)
    tier_top = models.FloatField(blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.billing_spec.name

    def fee_with_retirement_percent(self):
    	if self.fee_with_retirement is None:
    		return 0

    	return self.fee_with_retirement * 100

    def fee_without_retirement_percent(self):
    	if self.fee_without_retirement is None:
    		return 0
    		
    	return self.fee_without_retirement * 100
