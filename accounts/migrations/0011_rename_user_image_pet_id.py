# Generated by Django 4.1.6 on 2023-03-01 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_pet_profile_image_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='user',
            new_name='pet_id',
        ),
    ]
