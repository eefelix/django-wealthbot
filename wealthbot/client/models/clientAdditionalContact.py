from django.db import models

class ClientAdditionalContact(models.Model):
    class Meta:
    	db_table = 'client_additional_contacts'
    client = models.ForeignKey('user.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
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
    dependents = models.SmallIntegerField(blank=True, null=True)
    ssn_tin = models.CharField(max_length=20, blank=True, null=True)
    income_source = models.CharField(max_length=100, blank=True, null=True)
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    employer_address = models.CharField(max_length=255, blank=True, null=True)
    employment_city = models.CharField(max_length=255, blank=True, null=True)
    employment_state_id = models.IntegerField(default=0, blank=True, null=True)
    employment_zip = models.CharField(max_length=255, blank=True, null=True)
    is_senior_political_figure = models.BooleanField(null=True)
    senior_spf_name = models.CharField(max_length=255, blank=True, null=True)
    senior_political_title = models.CharField(max_length=255, blank=True, null=True)
    senior_account_owner_relationship = models.CharField(max_length=255, blank=True, null=True)
    senior_country_office = models.CharField(max_length=255, blank=True, null=True)
    is_publicly_traded_company = models.BooleanField(null=True)
    publicle_company_name = models.CharField(max_length=255, blank=True, null=True)
    publicle_address = models.CharField(max_length=255, blank=True, null=True)
    publicle_city = models.CharField(max_length=255, blank=True, null=True)
    publicle_state_id = models.IntegerField(default=0, blank=True, null=True)
    is_broker_security_exchange_person = models.BooleanField(null=True)
    broker_security_exchange_company_name = models.CharField(max_length=255, blank=True, null=True)
    broker_security_exchange_compliance_letter = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    TYPE_SPOUSE = 'spouse'
    TYPE_OTHER = 'other'
    TYPE_CHOICES = (
        (TYPE_SPOUSE, 'spouse'),
        (TYPE_OTHER, 'other'),
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    spouse_first_name = models.CharField(max_length=255, blank=True, null=True)
    spouse_middle_name = models.CharField(max_length=255, blank=True, null=True)
    spouse_last_name = models.CharField(max_length=255, blank=True, null=True)
    spouse_birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.first_name
