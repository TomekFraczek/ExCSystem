# Generated by Django 2.1.4 on 2018-12-10 04:00

import core.models.FileModels
import core.models.MemberModels
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('core', '0001_initial_server'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlreadyUploadedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('picture', models.ImageField(default='shaka.webp', upload_to=core.models.FileModels.get_upload_path)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('image_type', models.CharField(choices=[('member', 'Member Profile Picture'), ('gear', 'Gear Image'), ('other', 'Other Image')], max_length=10)),
                ('sub_type', models.CharField(default='Unknown', help_text='Specific image category: i.e. Skis, Tent, Sleeping Bag etc.', max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='member',
            name='picture',
        ),
        migrations.AddField(
            model_name='member',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='member',
            name='image',
            field=models.ImageField(blank=True, default='shaka.webp', upload_to=core.models.MemberModels.get_profile_pic_upload_location, verbose_name='Profile Picture'),
        ),
        migrations.AddField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
        migrations.AddField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.CharField(default='Unset', max_length=30),
        ),
        migrations.AddField(
            model_name='gear',
            name='image',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.AlreadyUploadedImage'),
            preserve_default=False,
        ),
    ]
