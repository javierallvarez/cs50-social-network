# Generated by Django 3.2.9 on 2022-04-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_post_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='img',
        ),
        migrations.AddField(
            model_name='profile',
            name='banner_side',
            field=models.CharField(blank=True, default=None, max_length=180, null=True),
        ),
    ]
