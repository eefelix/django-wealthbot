from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.db import models
from django.contrib.auth.models import AbstractUser
from client.models import ClientPortfolio
from .role import Role
from . import Profile

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

    def getGroupsAsString(self):
        groupNames = []
        for group in self.groups.all():
            groupNames.append(group.name)
        if len(groupNames) > 0:
            return ", ".join(groupNames)
        else:
            return "No Groups"

    def getActivityMessage(self):
        message = None
        if self.role_set.filter(name='ROLE_CLIENT').exists and self.profile.client_status == Profile.CLIENT_STATUS_PROSPECT:
            message = 'Prospect Registered'

        return message

    def withEdit(self):
        return not self.hasApprovedPortfolio()

    def hasApprovedPortfolio(self):
        if not self.role_set.filter(name='ROLE_CLIENT').exists:
            raise Http404("User has not role: ROLE_CLIENT")

        for clientPortfolio in self.clientportfolio_set.all():
            if clientPortfolio.is_active:
                return clientPortfolio.isClientAccepted()

        return False

    @classmethod
    def findClientsByRia(cls, ria):
        user_profile = Profile.objects.filter(ria_user=ria)
        role = Role.objects.get(name='ROLE_CLIENT')
        return User.objects.filter(profile__in=user_profile, role=role)

    @classmethod
    def findOrderedProspectsByRia(cls, ria):
        # Skip implementing order by client accounts value_sum / group / step at this moment
        user_profile = Profile.objects.filter(
            ria_user=ria,
            client_status=Profile.CLIENT_STATUS_PROSPECT
        )
        role = Role.objects.get(name='ROLE_CLIENT')
        client_set = User.objects.filter(
            profile__in=user_profile,
            role=role
        ).order_by('last_name', 'first_name')

        clientsData = []
        for client in client_set:
            clientAccounts = client.clientAccounts.all()
            value_sum = 0
            for account in clientAccounts:
                value_sum += account.valueSum()
            data = {
                'client': client,
                'value_sum': value_sum,
            }
            clientsData.append(data)

        return clientsData

    @classmethod
    def findClientsWithNotApprovedPortfolioByRia(cls, ria):
        user_profile = Profile.objects.filter(
            ria_user=ria, 
        )
        client_portfolio = ClientPortfolio.objects.filter(
            status=ClientPortfolio.STATUS_PROPOSED, 
            is_active=True
        )
        return User.objects.filter(
            profile__in=user_profile,
            clientportfolio__in=client_portfolio
        )