# Generated by Django 4.0.4 on 2022-04-22 20:36

import core.models.FileModels
import core.models.MemberModels
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_add_staffer_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='emergency_contact_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Contact Name'),
        ),
        migrations.AddField(
            model_name='member',
            name='emergency_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Best Email'),
        ),
        migrations.AddField(
            model_name='member',
            name='emergency_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='member',
            name='emergency_relation',
            field=models.CharField(max_length=50, null=True, verbose_name='Relationship'),
        ),
        migrations.AlterField(
            model_name='alreadyuploadedimage',
            name='picture',
            field=models.ImageField(default='uwcclogo.png', upload_to=core.models.FileModels.get_upload_path),
        ),
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, default='uwcclogo.png', null=True, upload_to=core.models.MemberModels.get_profile_pic_upload_location, verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='staffer',
            name='exc_email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Official Club Email'),
        ),
        migrations.AlterField(
            model_name='staffer',
            name='title',
            field=models.CharField(default='Climbing Club Staff!', max_length=30, verbose_name='Position Title'),
        ),
    ]
