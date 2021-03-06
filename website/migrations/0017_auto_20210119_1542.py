# Generated by Django 3.1.5 on 2021-01-19 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_auto_20210119_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='featureditem',
        ),
        migrations.RemoveField(
            model_name='casestudy',
            name='featureditem',
        ),
        migrations.RemoveField(
            model_name='component',
            name='featureditem',
        ),
        migrations.RemoveField(
            model_name='product',
            name='featureditem',
        ),
        migrations.RemoveField(
            model_name='reasonstochoose',
            name='featureditem',
        ),
        migrations.RemoveField(
            model_name='researchapplication',
            name='featureditem',
        ),
        migrations.AddField(
            model_name='application',
            name='body_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='application',
            name='title',
            field=models.CharField(default='Old Thing', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='casestudy',
            name='body_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='title',
            field=models.CharField(default='Study', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='body_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='component',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='component',
            name='title',
            field=models.CharField(default='Component', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='body_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(default='Product', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonstochoose',
            name='body_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reasonstochoose',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reasonstochoose',
            name='title',
            field=models.CharField(default='Reason', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='researchapplication',
            name='body_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='researchapplication',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='researchapplication',
            name='title',
            field=models.CharField(default='ResearchApp', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('SO', 'Software'), ('3D', '3D Measurement'), ('OT', 'Other'), ('DH', 'Data Hubs'), ('CS', 'CMA Systems')], default='OT', max_length=2),
        ),
        migrations.DeleteModel(
            name='FeaturedItem',
        ),
    ]
