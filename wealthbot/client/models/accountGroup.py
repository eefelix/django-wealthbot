from django.db import models

class AccountGroup(models.Model):
    class Meta:
    	db_table = 'client_account_groups'
    # ENUM group choices
    GROUP_FINANCIAL_INSTITUTION = 'financial_institution'
    GROUP_DEPOSIT_MONEY = 'deposit_money'
    GROUP_OLD_EMPLOYER_RETIREMENT = 'old_employer_retirement'
    GROUP_EMPLOYER_RETIREMENT = 'employer_retirement'
    _groups = [
	    (GROUP_FINANCIAL_INSTITUTION, 'financial_institution'),
	    (GROUP_DEPOSIT_MONEY, 'deposit_money'),
	    (GROUP_OLD_EMPLOYER_RETIREMENT, 'old_employer_retirement'),
	    (GROUP_EMPLOYER_RETIREMENT, 'employer_retirement'),
    ]
    name = models.CharField(max_length=255, choices=_groups)

    @classmethod
    def getGroupChoices(cls):
    	return cls._groups

    def __str__(self):
        return str(self.pk) + ": " + self.name
