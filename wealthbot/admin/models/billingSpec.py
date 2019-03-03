from django.db import models

class BillingSpec(models.Model):
    class Meta:
    	db_table = 'billing_spec'
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    master = models.BooleanField(default=True)
    TYPE_TIER = 1
    TYPE_FLAT = 2
    TYPE_CHOICES = (
	    (TYPE_TIER, '1: Tier'),
    	(TYPE_FLAT, '2: Flat'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)
    minimalFee = models.FloatField()
    feeTier = []

    def __str__(self):
    	return str(self.pk) + ": " + self.name

    def calcFeeTier(self):
        bottom = 0
        self.feeTier = []
        for fee in self.fees.all():
            tier = {'fee': fee, 'bottom': bottom}
            self.feeTier.append(tier)
            bottom = fee.tier_top + 0.01
