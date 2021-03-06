# Generated by Django 3.1.5 on 2021-02-16 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0089_auto_20210215_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='source',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
