from django.db import models

class AccountType(models.Model):
    class Meta:
    	db_table = 'client_account_types'
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk) + ": " + self.name
