# Generated by Django 2.1.4 on 2019-01-23 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_auto_20190120_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientaccount',
            name='system_type',
            field=models.IntegerField(default=1),
        ),
    ]
