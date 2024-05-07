# Generated by Django 4.1 on 2023-12-20 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpenAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=6)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=10)),
                ('district', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('occupation', models.CharField(max_length=255)),
                ('parent_name', models.CharField(max_length=255)),
                ('nominee_name', models.CharField(max_length=255)),
                ('nominee_relationship', models.CharField(max_length=255)),
            ],
        ),
    ]
