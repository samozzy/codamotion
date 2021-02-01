# Generated by Django 3.1.5 on 2021-01-20 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_auto_20210120_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
    ]
