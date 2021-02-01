# Generated by Django 3.1.5 on 2021-01-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20210118_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('SO', 'Software'), ('DH', 'Data Hubs'), ('OT', 'Other'), ('3D', '3D Measurement'), ('CS', 'CMA Systems')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='role',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]
