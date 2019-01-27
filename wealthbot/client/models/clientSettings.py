from django.db import models
from user.models import User

class ClientSettings(models.Model):
    class Meta:
    	db_table = 'client_settings'
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    stop_tlh_value = models.FloatField(blank=True, null=True)
    CLIENT_TYPE_NEW = 'new'
    CLIENT_TYPE_CURRENT = 'current'
    CLIENT_TYPE_CHOICES = (
    	(CLIENT_TYPE_NEW, 'new'),
    	(CLIENT_TYPE_CURRENT, 'current')
    )
    client_type = models.CharField(max_length=10, choices=CLIENT_TYPE_CHOICES, 
    	default=CLIENT_TYPE_NEW)

    def __str__(self):
    	return str(self.pk) + ": " + self.client.username
