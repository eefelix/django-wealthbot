from django.db import models

class SecurityType(models.Model):
    class Meta:
    	db_table = 'security_types'
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.name
