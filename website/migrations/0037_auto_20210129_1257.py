# Generated by Django 3.1.5 on 2021-01-29 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0036_auto_20210125_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('H', 'Header'), ('F', 'Footer')], default='H', max_length=1, unique=True)),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4),
        ),
        migrations.AddField(
            model_name='page',
            name='menu',
            field=models.ManyToManyField(to='website.SiteMenu'),
        ),
    ]
