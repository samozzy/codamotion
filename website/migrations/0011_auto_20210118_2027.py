# Generated by Django 3.1.5 on 2021-01-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20210118_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='year',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('CS', 'CMA Systems'), ('SO', 'Software'), ('DH', 'Data Hubs'), ('OT', 'Other'), ('3D', '3D Measurement')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('ADVS', 'Advisors'), ('MGMT', 'Management')], default='KEYC', max_length=4),
        ),
    ]
