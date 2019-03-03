# Generated by Django 2.1.4 on 2019-02-02 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190130_2240'),
        ('client', '0009_auto_20190124_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(1, 'Paperwork'), (2, 'Alert')], default=1)),
                ('object_id', models.IntegerField(blank=True, null=True)),
                ('object_type', models.CharField(max_length=255)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('message_code', models.CharField(choices=[('p9', 'Portfolio Proposal'), ('p10', 'Initial Rebalance'), ('p1', 'New Account'), ('p6', 'Banking Information Update'), ('p5', 'Address Update'), ('p3', 'Rollover'), ('p2', 'Transfer'), ('p7', 'New/Update Contributions'), ('p4', 'New/Update Beneficiary'), ('p8', 'New/Update Distributions'), ('a3', 'Closed Account'), ('a1', 'New Retirement Account')], max_length=3)),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'new'), (1, 'in progress'), (2, 'pending'), (3, 'completed')], default=0)),
                ('client_status', models.SmallIntegerField(choices=[(0, ''), (1, 'envelope created'), (2, 'envelope opened'), (3, 'envelope completed'), (4, 'portfolio proposed'), (5, 'client accepted portfolio'), (6, 'account opened'), (7, 'account funded')], default=0)),
                ('is_archived', models.BooleanField(default=False)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('submitted', models.DateField(auto_now_add=True)),
                ('client_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'workflow',
            },
        ),
        migrations.AlterField(
            model_name='clientportfolio',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='clientportfolio',
            name='status',
            field=models.CharField(choices=[('proposed', 'proposed'), ('advisor approved', 'advisor approved'), ('client accepted', 'client accepted')], default='proposed', max_length=20),
        ),
    ]
