# Generated by Django 2.1.4 on 2019-01-16 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_accountgroup_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountGroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.AccountGroup')),
            ],
            options={
                'db_table': 'client_account_group_types',
            },
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'client_account_types',
            },
        ),
        migrations.AddField(
            model_name='accountgrouptype',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.AccountType'),
        ),
        migrations.AddField(
            model_name='clientaccount',
            name='groupType',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='client.AccountGroupType'),
            preserve_default=False,
        ),
    ]