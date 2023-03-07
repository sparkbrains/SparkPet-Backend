# Generated by Django 4.1.6 on 2023-03-07 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_petprofile_upload_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petprofile',
            old_name='petbreed',
            new_name='breed',
        ),
        migrations.RenameField(
            model_name='petprofile',
            old_name='petage',
            new_name='pet_age',
        ),
        migrations.RenameField(
            model_name='petprofile',
            old_name='petname',
            new_name='pet_name',
        ),
        migrations.RenameField(
            model_name='petprofile',
            old_name='pettype',
            new_name='pet_type',
        ),
        migrations.RemoveField(
            model_name='petprofile',
            name='petgender',
        ),
        migrations.RemoveField(
            model_name='petprofile',
            name='petimage',
        ),
        migrations.AddField(
            model_name='petprofile',
            name='pet_gender',
            field=models.CharField(blank=True, choices=[('M', 'MALE'), ('F', 'FEMALE')], max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=11, max_length=254, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='pet_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='petprofile', to='accounts.petprofile'),
        ),
    ]