from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Role
from client.models import ClientSettings, ClientAdditionalContact, ClientQuestionnaireAnswer
from client.models import AccountGroup, AccountType, AccountGroupType, ClientAccount
from client.models import SystemAccount, ClientPortfolio
from admin.models import BillingSpec, CeModel, CeModelEntity, AssetClass, Subclass
from admin.models import Security, SecurityAssignment, SecurityType, Fee
from ria.models import RiaCompanyInformation, RiskQuestion, RiskAnswer

class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('appointedBillingSpec',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(ClientSettings)
admin.site.register(ClientAdditionalContact)
admin.site.register(BillingSpec)
admin.site.register(Fee)
admin.site.register(CeModel)
admin.site.register(RiaCompanyInformation)
admin.site.register(RiskQuestion)
admin.site.register(RiskAnswer)
admin.site.register(ClientQuestionnaireAnswer)
admin.site.register(AccountGroup)
admin.site.register(AccountType)
admin.site.register(AccountGroupType)
admin.site.register(ClientAccount)
admin.site.register(SystemAccount)
admin.site.register(ClientPortfolio)
admin.site.register(CeModelEntity)
admin.site.register(AssetClass)
admin.site.register(Subclass)
admin.site.register(Security)
admin.site.register(SecurityAssignment)
admin.site.register(SecurityType)
# Register your models here.
