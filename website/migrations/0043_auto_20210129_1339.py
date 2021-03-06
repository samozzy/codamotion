# Generated by Django 3.1.5 on 2021-01-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0042_auto_20210129_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='menu',
            field=models.ManyToManyField(blank=True, to='website.SiteMenu'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
    ]
