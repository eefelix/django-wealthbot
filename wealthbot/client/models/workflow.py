from django.db import models

class Workflow(models.Model):
    class Meta:
    	db_table = 'workflow'
    client_user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    # Constants for type column
    TYPE_PAPERWORK = 1
    TYPE_ALERT = 2
    TYPE_CHOICES = (
        (TYPE_PAPERWORK, 'Paperwork'),
        (TYPE_ALERT, 'Alert'),
    )
    type = models.SmallIntegerField(default=1, choices=TYPE_CHOICES)
    object_id = models.IntegerField(blank=True, null=True)
    object_type = models.CharField(max_length=255)
    message = models.CharField(max_length=255, blank=True, null=True)
    # Message code constants for paperwork
    MESSAGE_CODE_PAPERWORK_NEW_ACCOUNT = 'p1'
    MESSAGE_CODE_PAPERWORK_TRANSFER = 'p2'
    MESSAGE_CODE_PAPERWORK_ROLLOVER = 'p3'
    MESSAGE_CODE_PAPERWORK_UPDATE_BENEFICIARY = 'p4'
    MESSAGE_CODE_PAPERWORK_UPDATE_ADDRESS = 'p5'
    MESSAGE_CODE_PAPERWORK_UPDATE_BANKING_INFORMATION = 'p6'
    MESSAGE_CODE_PAPERWORK_UPDATE_CONTRIBUTIONS = 'p7'
    MESSAGE_CODE_PAPERWORK_UPDATE_DISTRIBUTIONS = 'p8'
    MESSAGE_CODE_PAPERWORK_PORTFOLIO_PROPOSED = 'p9'
    MESSAGE_CODE_PAPERWORK_INITIAL_REBALANCE = 'p10'
    _paperworkMessages = {
        MESSAGE_CODE_PAPERWORK_NEW_ACCOUNT: 'New Account',
        MESSAGE_CODE_PAPERWORK_TRANSFER: 'Transfer',
        MESSAGE_CODE_PAPERWORK_ROLLOVER: 'Rollover',
        MESSAGE_CODE_PAPERWORK_UPDATE_BENEFICIARY: 'New/Update Beneficiary',
        MESSAGE_CODE_PAPERWORK_UPDATE_ADDRESS: 'Address Update',
        MESSAGE_CODE_PAPERWORK_UPDATE_BANKING_INFORMATION: 'Banking Information Update',
        MESSAGE_CODE_PAPERWORK_UPDATE_CONTRIBUTIONS: 'New/Update Contributions',
        MESSAGE_CODE_PAPERWORK_UPDATE_DISTRIBUTIONS: 'New/Update Distributions',
        MESSAGE_CODE_PAPERWORK_PORTFOLIO_PROPOSED: 'Portfolio Proposal',
        MESSAGE_CODE_PAPERWORK_INITIAL_REBALANCE: 'Initial Rebalance',
    }
    # Message code constants for alerts
    MESSAGE_CODE_ALERT_NEW_RETIREMENT_ACCOUNT = 'a1'
    MESSAGE_CODE_ALERT_CLOSED_ACCOUNT = 'a3'
    _alertMessages = {
        MESSAGE_CODE_ALERT_NEW_RETIREMENT_ACCOUNT: 'New Retirement Account',
        MESSAGE_CODE_ALERT_CLOSED_ACCOUNT: 'Closed Account',
    }
    MESSAGE_CODE_CHOICES = list(_paperworkMessages.items()) + list(_alertMessages.items())
    message_code = models.CharField(max_length=3, choices=MESSAGE_CODE_CHOICES)
    note = models.CharField(max_length=1000, blank=True, null=True)
    # Constants for status column
    STATUS_NEW = 0
    STATUS_IN_PROGRESS = 1
    STATUS_PENDING = 2
    STATUS_COMPLETED = 3
    STATUS_CHOICES = (
        (STATUS_NEW, 'new'),
        (STATUS_IN_PROGRESS, 'in progress'),
        (STATUS_PENDING, 'pending'),
        (STATUS_COMPLETED, 'completed'),
    )
    status = models.SmallIntegerField(default=STATUS_NEW, choices=STATUS_CHOICES)
    # Constants for client status column
    CLIENT_STATUS_DEFAULT = 0
    CLIENT_STATUS_ENVELOPE_CREATED = 1
    CLIENT_STATUS_ENVELOPE_OPENED = 2
    CLIENT_STATUS_ENVELOPE_COMPLETED = 3
    CLIENT_STATUS_PORTFOLIO_PROPOSED = 4
    CLIENT_STATUS_PORTFOLIO_CLIENT_ACCEPTED = 5
    CLIENT_STATUS_ACCOUNT_OPENED = 6
    CLIENT_STATUS_ACCOUNT_FUNDED = 7
    CLIENT_STATUS_CHOICES = (
        (CLIENT_STATUS_DEFAULT, ''),
        (CLIENT_STATUS_ENVELOPE_CREATED, 'envelope created'),
        (CLIENT_STATUS_ENVELOPE_OPENED, 'envelope opened'),
        (CLIENT_STATUS_ENVELOPE_COMPLETED, 'envelope completed'),
        (CLIENT_STATUS_PORTFOLIO_PROPOSED, 'portfolio proposed'),
        (CLIENT_STATUS_PORTFOLIO_CLIENT_ACCEPTED, 'client accepted portfolio'),
        (CLIENT_STATUS_ACCOUNT_OPENED, 'account opened'),
        (CLIENT_STATUS_ACCOUNT_FUNDED, 'account funded'),
    )
    client_status = models.SmallIntegerField(default=CLIENT_STATUS_DEFAULT, choices=CLIENT_STATUS_CHOICES)
    is_archived = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + ": " + self.client.username

    # Skip implementing paper work count at this moment
    @classmethod
    def getPaperworkCountsByRia(cls, riaId):
        result = {
            'new': 0,
            'in_progress': 0,
            'pending': 0,
            'completed': 0,
        }

        return result
