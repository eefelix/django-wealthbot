# Generated by Django 2.1.4 on 2019-01-08 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20190108_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiaCompanyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('primary_first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('primary_last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('office', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state_id', models.IntegerField(blank=True, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=25, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True)),
                ('fax_number', models.CharField(blank=True, max_length=25, null=True)),
                ('contact_email', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.CharField(blank=True, max_length=255, null=True)),
                ('account_managed', models.IntegerField(blank=True, null=True)),
                ('is_allow_retirement_plan', models.BooleanField(blank=True, null=True)),
                ('minimum_billing_fee', models.FloatField(blank=True, null=True)),
                ('is_show_client_expected_asset_class', models.BooleanField(default=True)),
                ('clients_tax_bracket', models.FloatField(blank=True, null=True)),
                ('use_municipal_bond', models.BooleanField()),
                ('rebalanced_method', models.IntegerField(blank=True, null=True)),
                ('rebalanced_frequency', models.IntegerField(blank=True, null=True)),
                ('risk_adjustment', models.IntegerField(blank=True, null=True)),
                ('is_searchable_db', models.BooleanField(blank=True, null=True)),
                ('min_asset_size', models.FloatField(blank=True, null=True)),
                ('adv_copy', models.CharField(blank=True, max_length=255, null=True)),
                ('portfolio_model_id', models.IntegerField(blank=True, null=True)),
                ('activated', models.BooleanField(default=False)),
                ('transaction_amount', models.FloatField(blank=True, null=True)),
                ('transaction_amount_percent', models.FloatField(blank=True, null=True)),
                ('is_transaction_fees', models.BooleanField(blank=True, null=True)),
                ('is_transaction_minimums', models.BooleanField(blank=True, null=True)),
                ('is_transaction_redemption_fees', models.BooleanField(blank=True, null=True)),
                ('is_tax_loss_harvesting', models.BooleanField(blank=True, null=True)),
                ('is_show_expected_costs', models.BooleanField(default=True)),
                ('tax_loss_harvesting', models.FloatField(blank=True, null=True)),
                ('tax_loss_harvesting_percent', models.FloatField(blank=True, null=True)),
                ('tax_loss_harvesting_minimum', models.FloatField(blank=True, null=True)),
                ('tax_loss_harvesting_minimum_percent', models.FloatField(blank=True, null=True)),
                ('tlh_buy_back_original', models.BooleanField(default=False)),
                ('is_use_qualified_models', models.BooleanField(default=False)),
                ('portfolio_processing', models.IntegerField(blank=True, null=True)),
                ('allow_non_electronically_signing', models.BooleanField(blank=True, null=True)),
                ('stop_tlh_value', models.FloatField(blank=True, null=True)),
                ('relationship_type', models.IntegerField(choices=[(0, 'License Fee'), (1, 'TAMP')], default=0)),
                ('ria_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'ria_company_information',
            },
        ),
    ]