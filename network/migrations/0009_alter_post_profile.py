# Generated by Django 3.2.9 on 2022-04-20 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='network.profile'),
        ),
    ]