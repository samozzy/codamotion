# Generated by Django 3.1.5 on 2021-02-08 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0071_auto_20210208_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-submission_date'], 'verbose_name': 'Contact Form Response', 'verbose_name_plural': 'Contact Form Responses'},
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('MGMT', 'Management'), ('ADVS', 'Advisors'), ('KEYC', 'Key Contact')], default='KEYC', max_length=4),
        ),
    ]
