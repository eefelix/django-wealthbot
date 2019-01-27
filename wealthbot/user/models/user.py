from django.db import models
from django.contrib.auth.models import AbstractUser
from .role import Role

class User(AbstractUser):
    class Meta:
    	db_table = 'users'
    password_expired_at = models.DateTimeField(blank=True, null=True)
    master_client_id = models.IntegerField(default=0, blank=True, null=True)
    is_password_reset = models.BooleanField(blank=True, null=True)
    closed = models.DateTimeField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    appointedBillingSpec = models.ForeignKey('webo_admin.BillingSpec', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.pk) + ": " + self.username

    def hasRole(self, role):
        return self.role_set.filter(name=role.upper()).exists()

    def setRoles(self, roles):
        for role in roles:
            self.role_set.add(Role.objects.get(name=role))
        return self

    def getSpouse(self):
        for contact in self.clientadditionalcontact_set.all():
            if contact.type == ClientAdditionalContact.TYPE_SPOUSE:
                return contact
        return

    # Returns true if client is married and false otherwise.
    def isMarried(self):
        if hasattr(self, 'profile'):
            return self.profile.isMarried()
        else:
            return False

    def removeAdditionalContact(self, contact):
        if contact is not None:
            self.clientadditionalcontact_set.filter(pk=contact.id).delete()
