# Generated by Django 3.1.5 on 2021-02-19 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0096_auto_20210218_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='image',
        ),
        migrations.AddField(
            model_name='application',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='component',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='teammember',
            name='image_url',
            field=models.CharField(blank=True, help_text='Full path to an existing image. If using an internal link, in the format <code>/static/image/image.jpg</code>; if external, in the format <code>https://example.com/image.jpg</code>. Overridden by an image upload', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='sitemenu',
            name='title',
            field=models.CharField(choices=[('F', 'Footer'), ('H', 'Header')], default='H', max_length=1, unique=True),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='person_type',
            field=models.CharField(choices=[('MGMT', 'Management'), ('ADVS', 'Advisors'), ('KEYC', 'Key Contact')], default='KEYC', max_length=4),
        ),
    ]