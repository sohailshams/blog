# Generated by Django 4.1 on 2022-10-20 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('profile_img', models.ImageField(default='blank-profile.png', upload_to='profile_images')),
                ('location', models.CharField(blank=True, max_length=100)),
                ('user_bio', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]