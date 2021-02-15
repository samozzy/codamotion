# Generated by Django 3.1.5 on 2021-02-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0085_auto_20210215_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='case_study_link',
            field=models.ManyToManyField(to='website.CaseStudy'),
        ),
        migrations.AlterField(
            model_name='sitemenu',
            name='title',
            field=models.CharField(choices=[('H', 'Header'), ('F', 'Footer')], default='H', max_length=1, unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
    ]
