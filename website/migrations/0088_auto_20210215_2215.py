# Generated by Django 3.1.5 on 2021-02-15 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0087_auto_20210215_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='lead_text',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='sitemenu',
            name='title',
            field=models.CharField(choices=[('F', 'Footer'), ('H', 'Header')], default='H', max_length=1, unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('ADVS', 'Advisors'), ('KEYC', 'Key Contact'), ('MGMT', 'Management')], default='KEYC', max_length=4),
        ),
    ]
