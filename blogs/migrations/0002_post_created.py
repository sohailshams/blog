# Generated by Django 4.1 on 2022-08-14 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 14, 21, 33, 33, 629549, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]