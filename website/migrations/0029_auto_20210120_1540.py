# Generated by Django 3.1.5 on 2021-01-20 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0028_auto_20210120_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='company_text',
            field=models.TextField(help_text='About the company, eg. registration info, company number'),
        ),
        migrations.AlterField(
            model_name='reasonstochoose',
            name='category',
            field=models.CharField(choices=[('C', 'Clinical'), ('R', 'Research')], default='R', max_length=1),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('MGMT', 'Management'), ('KEYC', 'Key Contact'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
    ]
