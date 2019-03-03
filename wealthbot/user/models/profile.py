from django.db import models
from django.core.exceptions import PermissionDenied
from django.http import Http404
from client.models import ClientAdditionalContact

class Profile(models.Model):
    class Meta:
    	db_table = 'user_profiles'
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    ria_user = models.ForeignKey('user.User', related_name='ria', on_delete=models.CASCADE, blank=True, null=True)
    registration_step = models.IntegerField(default=0)
    company = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.IntegerField(default=0, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    is_different_address = models.BooleanField(null=True)
    mailing_street = models.CharField(max_length=255, blank=True, null=True)
    mailing_city = models.CharField(max_length=255, blank=True, null=True)
    mailing_state_id = models.IntegerField(default=0, blank=True, null=True)
    mailing_zip = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    CLIENT_MARITAL_STATUS_SINGLE = 'Single'
    CLIENT_MARITAL_STATUS_MARRIED = 'Married'
    CLIENT_MARITAL_STATUS_DIVORCED = 'Divorced'
    CLIENT_MARITAL_STATUS_SEPARATED = 'Separated'
    CLIENT_MARTIAL_STATUS_CHOICES = (
        (CLIENT_MARITAL_STATUS_SINGLE, 'Single'),
        (CLIENT_MARITAL_STATUS_MARRIED, 'Married'),
        (CLIENT_MARITAL_STATUS_DIVORCED, 'Divorced'),
        (CLIENT_MARITAL_STATUS_SEPARATED, 'Separated'),
    )
    marital_status = models.CharField(choices=CLIENT_MARTIAL_STATUS_CHOICES, max_length=20, blank=True, null=True)
    CLIENT_ANNUAL_INCOME_VALUE1 = '$0-$50,000'
    CLIENT_ANNUAL_INCOME_VALUE2 = '$50,001-$75,000'
    CLIENT_ANNUAL_INCOME_VALUE3 = '$75,001-$100,000'
    CLIENT_ANNUAL_INCOME_VALUE4 = '$100,001-$150,000'
    CLIENT_ANNUAL_INCOME_VALUE5 = '$150,001-$250,000'
    CLIENT_ANNUAL_INCOME_VALUE6 = '$250,001 +'
    CLIENT_ANNUAL_INCOME_CHOICES = (
        (CLIENT_ANNUAL_INCOME_VALUE1, '$0-$50,000'),
        (CLIENT_ANNUAL_INCOME_VALUE2, '$50,001-$75,000'),
        (CLIENT_ANNUAL_INCOME_VALUE3, '$75,001-$100,000'),
        (CLIENT_ANNUAL_INCOME_VALUE4, '$100,001-$150,000'),
        (CLIENT_ANNUAL_INCOME_VALUE5, '$150,001-$250,000'),
        (CLIENT_ANNUAL_INCOME_VALUE6, '$250,001 +'),
    )
    annual_income = models.CharField(choices=CLIENT_ANNUAL_INCOME_CHOICES, max_length=50, blank=True, null=True)
    estimated_income_tax = models.CharField(max_length=50, blank=True, null=True)
    CLIENT_LIQUID_NET_WORTH_VALUE1 = '$0-$25,000'
    CLIENT_LIQUID_NET_WORTH_VALUE2 = '$25,001-$50,000'
    CLIENT_LIQUID_NET_WORTH_VALUE3 = '$50,001-$100,000'
    CLIENT_LIQUID_NET_WORTH_VALUE4 = '$100,001-$200,000'
    CLIENT_LIQUID_NET_WORTH_VALUE5 = '$200,001-$350,000'
    CLIENT_LIQUID_NET_WORTH_VALUE6 = '$350,001-$700,000'
    CLIENT_LIQUID_NET_WORTH_VALUE7 = '$700,001-$1,000,000'
    CLIENT_LIQUID_NET_WORTH_VALUE8 = '$1,000,000 +'
    CLIENT_LIQUID_NET_WORTH_CHOICES = (
        (CLIENT_LIQUID_NET_WORTH_VALUE1, '$0-$25,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE2, '$25,001-$50,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE3, '$50,001-$100,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE4, '$100,001-$200,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE5, '$200,001-$350,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE6, '$350,001-$700,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE7, '$700,001-$1,000,000'),
        (CLIENT_LIQUID_NET_WORTH_VALUE8, '$1,000,000 +'),
    )
    liquid_net_worth = models.CharField(choices=CLIENT_LIQUID_NET_WORTH_CHOICES, max_length=50, blank=True, null=True)
    CLIENT_EMPLOYMENT_TYPE_EMPLOYED = 'Employed'
    CLIENT_EMPLOYMENT_TYPE_SELF_EMPLOYED = 'Self-Employed'
    CLIENT_EMPLOYMENT_TYPE_RETIRED = 'Retired'
    CLIENT_EMPLOYMENT_TYPE_UNEMPLOYED = 'Unemployed'
    CLIENT_EMPLOYMENT_TYPE_CHOICES = (
        (CLIENT_EMPLOYMENT_TYPE_EMPLOYED, 'Employed'),
        (CLIENT_EMPLOYMENT_TYPE_SELF_EMPLOYED, 'Self-Employed'),
        (CLIENT_EMPLOYMENT_TYPE_RETIRED, 'Retired'),
        (CLIENT_EMPLOYMENT_TYPE_UNEMPLOYED, 'Unemployed'),
    )
    employment_type = models.CharField(choices=CLIENT_EMPLOYMENT_TYPE_CHOICES, default=CLIENT_EMPLOYMENT_TYPE_EMPLOYED, max_length=50, blank=False, null=True)
    suggested_portfolio_id = models.IntegerField(default=0, blank=True, null=True)
    questionnaire_step = models.SmallIntegerField(default=0, blank=True, null=True)
    withdraw_age = models.IntegerField(default=0, blank=True, null=True)
    CLIENT_SOURCE_WEB = 'web'
    CLIENT_SOURCE_IN_HOUSE = 'in-house'
    CLIENT_SOURCE_CHOICES = (
        (CLIENT_SOURCE_WEB, 'web'),
        (CLIENT_SOURCE_IN_HOUSE, 'in-house'),
    )
    client_source = models.CharField(choices=CLIENT_SOURCE_CHOICES, max_length=10, blank=True, null=True)
    CLIENT_ACCOUNT_MANAGED_ACCOUNT = 1
    CLIENT_ACCOUNT_MANAGED_HOUSEHOLDER = 2
    CLIENT_ACCOUNT_MANAGED_CHOICES = (
        (CLIENT_ACCOUNT_MANAGED_ACCOUNT, 'Account Level'),
        (CLIENT_ACCOUNT_MANAGED_HOUSEHOLDER, 'Householder Level'),
    )
    client_account_managed = models.SmallIntegerField(choices=CLIENT_ACCOUNT_MANAGED_CHOICES, blank=True, null=True)
    CLIENT_STATUS_PROSPECT = 1
    CLIENT_STATUS_CLIENT = 2
    CLIENT_STATUS_CHOICES = (
        (CLIENT_STATUS_PROSPECT, 'prospect'),
        (CLIENT_STATUS_CLIENT, 'client'),
    )
    client_status = models.SmallIntegerField(choices=CLIENT_STATUS_CHOICES, blank=True, null=True)
    PAYMENT_METHOD_DIRECT_DEBIT = 1
    PAYMENT_METHOD_OUTSIDE_PAYMENT = 2
    PAYMENT_METHOD_CHOICES = (
        (PAYMENT_METHOD_DIRECT_DEBIT, 'Direct debit'),
        (PAYMENT_METHOD_OUTSIDE_PAYMENT, 'Outside payment'),
    )
    paymentMethod = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=0, blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.user.username

    # Returns true if user is client with marital_status = 
    # CLIENT_MARITAL_STATUS_MARRIED and false otherwise.
    def isMarried(self):
        clientRole = 'ROLE_CLIENT'
        if not self.user.hasRole(role=clientRole):
            raise PermissionDenied('User does not have role: %s' % clientRole)

        status = self.marital_status
        if status == self.CLIENT_MARITAL_STATUS_MARRIED:
            return True

        return False

    clientRegistrationSteps = [
        'Created Login',
        'Risk questionnaire',
        'Information Intake',
        'Suggested Portfolio',
        'Advisor Approved Portfolio',
        'Approved Portfolio',
        'Application Screen',
        'Completed All Applications',
    ]

    def clientRegistrationStep(self):
        return self.clientRegistrationSteps[self.registration_step]

    # Get last_name
    def lastName(self):
        return self.last_name

    # Get first_name
    def firstName(self):
        return self.first_name

    # Get middle_name
    def middleName(self):
        return self.middle_name

    # Get birth_date
    def birthDate(self):
        return self.birth_date

    # Get marital_status
    def maritalStatus(self):
        return self.marital_status

    # Get spouse_first_name
    def spouseFirstName(self):
        for contact in self.user.clientadditionalcontact_set.all():
            if contact.type == ClientAdditionalContact.TYPE_SPOUSE:
                return contact.spouse_first_name
        return

    # Get spouse_middle_name
    def spouseMiddleName(self):
        for contact in self.user.clientadditionalcontact_set.all():
            if contact.type == ClientAdditionalContact.TYPE_SPOUSE:
                return contact.spouse_middle_name
        return

    # Get spouse_last_name
    def spouseLastName(self):
        for contact in self.user.clientadditionalcontact_set.all():
            if contact.type == ClientAdditionalContact.TYPE_SPOUSE:
                return contact.spouse_last_name
        return

    # Get spouse_birth_date
    def spouseBirthDate(self):
        for contact in self.user.clientadditionalcontact_set.all():
            if contact.type == ClientAdditionalContact.TYPE_SPOUSE:
                return contact.spouse_birth_date
        return

    # Get phone_number
    def phoneNumber(self):
        return self.phone_number

    # Get employment_type
    def employmentType(self):
        return self.employment_type

    # Get annual_income
    def annualIncome(self):
        return self.annual_income

    # Get liquid_net_worth
    def liquidNetWorth(self):
        return self.liquid_net_worth

    # Get estimated_income_tax in percent format
    def estimatedIncomeTaxPercent(self):
        return "{0:.0%}".format(float(self.estimated_income_tax))

    # Get client_account_managed as string.
    def clientAccountManagedAsString(self):
        level = self.client_account_managed
        if level is None:
            self.ria_user.riacompanyinformation.getAccountManagementAsString()

        for choice in self.CLIENT_ACCOUNT_MANAGED_CHOICES:
            if choice[0] == level:
                return choice[1].lower()

        raise Http404("Value of client account managed for key : %d doesn't exist." % level)
        return
