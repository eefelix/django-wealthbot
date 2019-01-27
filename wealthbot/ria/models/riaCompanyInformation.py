from django.db import models
from user.models import User
from admin.models import CeModel

class RiaCompanyInformation(models.Model):
    class Meta:
    	db_table = 'ria_company_information'
    ria_user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    primary_first_name = models.CharField(max_length=255, blank=True, null=True)
    primary_last_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    office = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    zipcode = models.CharField(max_length=25, blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    fax_number = models.CharField(max_length=25, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    account_managed = models.IntegerField(blank=True, null=True)
    is_allow_retirement_plan = models.BooleanField(blank=True, null=True)
    minimum_billing_fee = models.FloatField(blank=True, null=True)
    is_show_client_expected_asset_class = models.BooleanField(default=True)
    clients_tax_bracket = models.FloatField(blank=True, null=True)
    use_municipal_bond = models.BooleanField()
    rebalanced_method = models.IntegerField(blank=True, null=True)
    rebalanced_frequency = models.IntegerField(blank=True, null=True)
    risk_adjustment = models.IntegerField(blank=True, null=True)
    is_searchable_db = models.BooleanField(blank=True, null=True)
    min_asset_size = models.FloatField(blank=True, null=True)
    adv_copy = models.CharField(max_length=255, blank=True, null=True)
    portfolio_model = models.ForeignKey(CeModel, on_delete=models.CASCADE, blank=True, null=True)
    activated = models.BooleanField(default=False)
    transaction_amount = models.FloatField(blank=True, null=True)
    transaction_amount_percent = models.FloatField(blank=True, null=True)
    is_transaction_fees = models.BooleanField(blank=True, null=True)
    is_transaction_minimums = models.BooleanField(blank=True, null=True)
    is_transaction_redemption_fees = models.BooleanField(blank=True, null=True)
    is_tax_loss_harvesting = models.BooleanField(blank=True, null=True)
    is_show_expected_costs = models.BooleanField(default=True)
    tax_loss_harvesting = models.FloatField(blank=True, null=True)
    tax_loss_harvesting_percent = models.FloatField(blank=True, null=True)
    tax_loss_harvesting_minimum = models.FloatField(blank=True, null=True)
    tax_loss_harvesting_minimum_percent = models.FloatField(blank=True, null=True)
    tlh_buy_back_original = models.BooleanField(default=False)
    is_use_qualified_models = models.BooleanField(default=False)
    portfolio_processing = models.IntegerField(blank=True, null=True)
    allow_non_electronically_signing = models.BooleanField(blank=True, null=True)
    stop_tlh_value = models.FloatField(blank=True, null=True)
    RELATIONSHIP_TYPE_LICENSE_FEE = 0
    RELATIONSHIP_TYPE_TAMP = 1
    RELATIONSHIP_TYPE_CHOICES = (
        (RELATIONSHIP_TYPE_LICENSE_FEE, 'License Fee'),
        (RELATIONSHIP_TYPE_TAMP, 'TAMP'),
    )
    relationship_type = models.IntegerField(choices=RELATIONSHIP_TYPE_CHOICES, 
        default=RELATIONSHIP_TYPE_LICENSE_FEE)

    def __str__(self):
    	return self.name
