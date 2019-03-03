from django.db import models
from admin.models import CeModel

class ClientPortfolio(models.Model):
    class Meta:
    	db_table = 'client_portfolio'
    client = models.ForeignKey('user.User', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(CeModel, on_delete=models.CASCADE)
    # ENUM values status column
    STATUS_PROPOSED = 'proposed'
    STATUS_ADVISOR_APPROVED = 'advisor approved'
    STATUS_CLIENT_ACCEPTED = 'client accepted'
    STATUS_CHOICES = (
        (STATUS_PROPOSED, 'proposed'),
        (STATUS_ADVISOR_APPROVED, 'advisor approved'),
        (STATUS_CLIENT_ACCEPTED, 'client accepted'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PROPOSED)
    is_active = models.BooleanField(default=True)
    approved_at = models.DateField(blank=True, null=True)
    accepted_at = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + ": " + self.client.username + ' - ' + self.portfolio.name

    # Is proposed portfolio.
    def isProposed(self):
        return (self.status == self.STATUS_PROPOSED)
        
    # Is advisor approved portfolio.
    def isAdvisorApproved(self):
        return (self.status == self.STATUS_ADVISOR_APPROVED)

    # Is client accepted portfolio.
    def isClientAccepted(self):
        return (self.status == self.STATUS_CLIENT_ACCEPTED)
    