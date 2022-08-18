# Generated by Django 4.1 on 2022-08-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_post_updated_alter_post_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='role',
            field=models.CharField(choices=[('owner', 'Owner'), ('viewer', 'Viewer')], default='owner', max_length=20),
        ),
    ]