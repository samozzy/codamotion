# Generated by Django 3.1.5 on 2021-01-18 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20210118_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_type', models.CharField(choices=[('KEYC', 'Key Contact'), ('MGMT', 'Management'), ('ADVS', 'Advisors')], default='KEYC', max_length=4)),
                ('person_name', models.CharField(max_length=200)),
                ('headshot', models.ImageField(blank=True, null=True, upload_to='')),
                ('role', models.CharField(max_length=140)),
                ('bio', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Team_Member',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('SO', 'Software'), ('DH', 'Data Hubs'), ('OT', 'Other'), ('CS', 'CMA Systems'), ('3D', '3D Measurement')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='reasons_to_choose',
            name='category',
            field=models.CharField(choices=[('R', 'Research'), ('C', 'Clinical')], default='R', max_length=1),
        ),
    ]
