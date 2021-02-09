# Generated by Django 3.1.5 on 2021-02-08 22:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0067_auto_20210208_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='submission_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 22, 48, 25, 631626, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('MGMT', 'Management'), ('KEYC', 'Key Contact'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
    ]