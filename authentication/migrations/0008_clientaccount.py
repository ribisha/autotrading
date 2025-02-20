# Generated by Django 4.1 on 2023-12-29 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0007_rename_user_masteraccount_user_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_full_name', models.CharField(blank=True, max_length=255)),
                ('client_profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('client_date_of_birth', models.DateField(blank=True, null=True)),
                ('client_gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('client_phone', models.CharField(blank=True, max_length=15)),
                ('client_email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('client_address', models.TextField(blank=True)),
                ('client_pincode', models.CharField(blank=True, max_length=10)),
                ('client_district', models.CharField(blank=True, max_length=255)),
                ('client_state', models.CharField(blank=True, max_length=255)),
                ('client_occupation', models.CharField(blank=True, max_length=255)),
                ('client_parent_name', models.CharField(blank=True, max_length=255)),
                ('client_nominee_name', models.CharField(blank=True, max_length=255)),
                ('client_nominee_relationship', models.CharField(blank=True, max_length=255)),
                ('user_client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
