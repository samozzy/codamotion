# Generated by Django 3.1.5 on 2021-01-30 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0048_auto_20210129_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='list_data',
            field=models.CharField(blank=True, choices=[('Movem', 'Movement Analysis - Clinical'), ('Movem', 'Movement Analysis - Research'), ('Case ', 'Case Studies'), ('Event', 'Events'), ('Team ', 'Team Members'), ('Histo', 'History'), ('Conta', 'Contact Distributors'), ('3D Me', '3D Measurement'), ('Softw', 'Software'), ('Data ', 'Data Hubs'), ('Other', 'Other Measurement Components'), ('Compl', 'Complete Movement Analysis Systems')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('ADVS', 'Advisors'), ('MGMT', 'Management'), ('KEYC', 'Key Contact')], default='KEYC', max_length=4),
        ),
    ]
