from django.db import models
from client.models import ClientAccount

class SystemAccount(models.Model):
    class Meta:
    	db_table = 'system_client_accounts'
    client = models.ForeignKey('user.User', on_delete=models.CASCADE)
    client_account = models.OneToOneField(ClientAccount, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=255)
    account_description = models.CharField(max_length=255, blank=True, null=True)
    # Constants for type column
    TYPE_PERSONAL_INVESTMENT = 1
    TYPE_JOINT_INVESTMENT = 2
    TYPE_ROTH_IRA = 3
    TYPE_TRADITIONAL_IRA = 4
    TYPE_RETIREMENT = 5
    TYPE_CHOICES = (
        (TYPE_PERSONAL_INVESTMENT, 'Personal Investment Account'),
        (TYPE_JOINT_INVESTMENT, 'Joint Investment Account'),
        (TYPE_ROTH_IRA, 'Roth IRA'),
        (TYPE_TRADITIONAL_IRA, 'Traditional IRA'),
        (TYPE_RETIREMENT, 'Retirement Account'),
    )
    type = models.SmallIntegerField(default=1, choices=TYPE_CHOICES)
    # Constants for status column
    STATUS_REGISTERED = 'registered'
    STATUS_ACTIVE = 'active'
    STATUS_INIT_REBALANCE = 'init rebalance'
    STATUS_INIT_REBALANCE_COMPLETE = 'init rebalance complete'
    STATUS_REBALANCED = 'rebalanced'
    STATUS_ANALYZED = 'account analyzed'
    STATUS_CLOSED = 'account closed'
    STATUS_WAITING_ACTIVATION = 'waiting activation'
    STATUS_CHOICES = (
        (STATUS_REGISTERED, 'registered'),
        (STATUS_ACTIVE, 'active'),
        (STATUS_INIT_REBALANCE, 'init rebalance'),
        (STATUS_INIT_REBALANCE_COMPLETE, 'init rebalance complete'),
        (STATUS_REBALANCED, 'rebalanced'),
        (STATUS_ANALYZED, 'account analyzed'),
        (STATUS_CLOSED, 'account closed'),
        (STATUS_WAITING_ACTIVATION, 'waiting activation'),
    )
    status = models.CharField(default=STATUS_REGISTERED, max_length=50, choices=STATUS_CHOICES)
    source = models.CharField(default='sample', max_length=45, blank=True, null=True)

    def __str__(self):
        return str(self.pk) + ": " + self.client.username
