# Generated by Django 4.1.6 on 2023-03-07 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_image_pet_profile_alter_petprofile_petgender'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='pet_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pet_name', to='accounts.petprofile'),
            preserve_default=False,
        ),
    ]