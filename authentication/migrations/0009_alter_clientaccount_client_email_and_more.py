# Generated by Django 4.1 on 2023-12-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_clientaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='client_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='clientaccount',
            name='client_profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='client_profile_images/'),
        ),
    ]
