from django.db import models
from django.contrib.auth.models import Group

class GroupOwner(models.Model):
    class Meta:
    	db_table = 'group_owner'
    ria_user = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
    	return str(self.pk) + ": " + self.group.name
