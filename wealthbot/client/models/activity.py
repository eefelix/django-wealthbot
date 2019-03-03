from django.db import models

class Activity(models.Model):
    class Meta:
    	db_table = 'activity'
    client_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='clientUserActivities')
    CLIENT_STATUS_PROSPECT = 1
    CLIENT_STATUS_CLIENT = 2
    CLIENT_STATUS_CHOICES = (
        (CLIENT_STATUS_PROSPECT, 'prospect'),
        (CLIENT_STATUS_CLIENT, 'client'),
    )
    client_status = models.SmallIntegerField(choices=CLIENT_STATUS_CHOICES, blank=True, null=True)
    ria_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='riaUserActivities')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(default='Prospect Registered', max_length=255)
    is_show_ria = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + ": " + self.client_user.username
