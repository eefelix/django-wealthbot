# Generated by Django 2.1.4 on 2019-02-15 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190130_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='client_account_managed',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Account Level'), (2, 'Householder Level')], null=True),
        ),
    ]
