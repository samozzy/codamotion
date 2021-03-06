# Generated by Django 3.1.5 on 2021-02-01 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0061_auto_20210201_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitemenu',
            name='title',
            field=models.CharField(choices=[('H', 'Header'), ('F', 'Footer')], default='H', max_length=1, unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('ADVS', 'Advisors'), ('KEYC', 'Key Contact'), ('MGMT', 'Management')], default='KEYC', max_length=4),
        ),
    ]
