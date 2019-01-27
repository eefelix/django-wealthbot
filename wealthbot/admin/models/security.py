from django.db import models

class Security(models.Model):
    class Meta:
    	db_table = 'securities'
    security_type = models.ForeignKey('webo_admin.SecurityType', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255, unique=True)
    expense_ratio = models.FloatField(blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.name
