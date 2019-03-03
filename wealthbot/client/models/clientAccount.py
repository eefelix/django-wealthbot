from django.db import models
from django.db.models import Q
from client.models import AccountGroupType, AccountGroup

class ClientAccount(models.Model):
    class Meta:
    	db_table = 'client_accounts'
    client = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='clientAccounts')
    groupType = models.ForeignKey(AccountGroupType, on_delete=models.CASCADE)
    financial_institution = models.CharField(max_length=255, blank=True, null=True)
    value = models.FloatField()
    monthly_contributions = models.FloatField(blank=True, null=True)
    monthly_distributions = models.FloatField(blank=True, null=True)
    sas_cash = models.FloatField(blank=True, null=True)
    process_step = models.IntegerField(default=0)
    step_action = models.CharField(max_length=255, blank=True, null=True)
    is_pre_saved = models.BooleanField(default=False)
    system_type = models.IntegerField(default=1)
    consolidator = models.ForeignKey('client.ClientAccount', on_delete=models.CASCADE, blank=True, null=True, related_name='consolidatedAccounts')
    unconsolidated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk) + ": " + self.client.username

    def activity(self):
        return {
            AccountGroup.GROUP_FINANCIAL_INSTITUTION : 'Transfer',
            AccountGroup.GROUP_DEPOSIT_MONEY : 'New Account',
            AccountGroup.GROUP_OLD_EMPLOYER_RETIREMENT : 'Rollover',
            AccountGroup.GROUP_EMPLOYER_RETIREMENT : 'Advice',
        }.get(self.groupType.group.name, None)

    # Get sum of the consolidated accounts values or value if account is
    # not consolidated.
    def valueSum(self):
        # Skip implementing consolidated accounts calc at this moment
        sum = self.value

        return sum

    # Get sum of the consolidated accounts monthly_contributions or
    # monthly_contribution if account is not consolidated.
    def contributionsSum(self):
        # Skip implementing consolidated accounts calc at this moment
        sum = self.monthly_contributions

        return sum

    # Get sum of the consolidated accounts monthly_distributions or
    # monthly_distribution if account is not consolidated.
    def distributionsSum(self):
        # Skip implementing consolidated accounts calc at this moment
        sum = self.monthly_distributions

        return sum

    @classmethod
    def getTotalScoreByClient(cls, client):
        accounts = ClientAccount.objects.filter(client=client)

        result = {
            'value': 0,
            'monthly_contributions': 0,
            'monthly_distributions': 0,
            'sas_cash': 0,
        }
        for account in accounts:
            if account.value is not None:
                result['value'] += account.value
            if account.monthly_contributions is not None:
                result['monthly_contributions'] += account.monthly_contributions
            if account.monthly_distributions is not None:
                result['monthly_distributions'] += account.monthly_distributions
            if account.sas_cash is not None:
                result['sas_cash'] += account.sas_cash

        return result

    @classmethod
    def findConsolidatedAccountsByClient(cls, client):
        return ClientAccount.objects.filter(
            Q(client=client) &
            (
                Q(unconsolidated=True)|
                Q(consolidator=None)
            )
        )

    @classmethod
    def hasRetirementAccount(cls, client):
        retirementAccounts = cls.getRetirementAccountsByClient(client=client)

        if retirementAccounts.count() > 0:
            return True
        else:
            return False

    @classmethod
    def getRetirementAccountsByClient(cls, client):
        retirementAccounts = cls.findByClientAndGroup(client=client, 
            group=AccountGroup.GROUP_EMPLOYER_RETIREMENT)

        return retirementAccounts

    @classmethod
    def findByClientAndGroup(cls, client, group):
        selected_group = AccountGroup.objects.get(name=group)
        selected_groupType = AccountGroupType.objects.filter(group=selected_group)
        return ClientAccount.objects.filter(client=client,
            groupType__in=selected_groupType)

    # Get name of group of account.
    def getGroupName(self):
        groupType = self.groupType

        if groupType is None:
            groupName = None
        else:
            if groupType.group is None:
                groupName = None
            else:
                groupName = groupType.group.name

        return groupName

    # Get unconsolidated.
    def getUnconsolidated(self):
        return unconsolidated

    # Get consolidator_id.
    def getConsolidatorId(self):
        if self.consolidator is not None:
            return self.consolidator.pk
        else:
            return None
