# Generated by Django 4.1.6 on 2023-03-01 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_rename_user_image_pet_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='pet_id',
            new_name='pet_profile',
        ),
    ]
