# Generated by Django 2.1.4 on 2019-01-12 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_appointedbillingspec'),
        ('ria', '0003_auto_20190112_0955'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientQuestionnaireAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ria.RiskAnswer')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ria.RiskQuestion')),
            ],
            options={
                'db_table': 'client_questionnaire_answers',
            },
        ),
    ]