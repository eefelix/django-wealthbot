from django.db import models
from client.models import AccountGroup, AccountType

class AccountGroupType(models.Model):
    class Meta:
    	db_table = 'client_account_group_types'
    group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE)
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk) + ": " + self.group.name + " - " + self.type.name
