# Generated by Django 4.1.6 on 2023-03-01 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_petprofile_petimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='pet_profile',
            new_name='user',
        ),
    ]
