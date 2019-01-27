from django.db import models
from django.contrib.auth.models import Group

class Role(models.Model):
    class Meta:
    	db_table = 'roles'
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField('user.User')
    groups = models.ManyToManyField(Group)

    def __str__(self):
    	return self.name
