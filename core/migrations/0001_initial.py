# Generated by Django 2.0.7 on 2018-08-16 05:30

import core.models.TransactionModels
import core.models.fields.RFIDField
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('rfid', core.models.fields.RFIDField.RFIDField(verbose_name='RFID')),
                ('picture', models.ImageField(null=True, upload_to='ProfilePics/%Y/', verbose_name='Profile Picture')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('date_expires', models.DateField()),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=100)),
                ('answer_phrase', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('requirements', models.TextField(verbose_name='Minimum Certification Requirements')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.IntegerField(choices=[(0, 'In Stock'), (1, 'Checked Out'), (2, 'Broken'), (3, 'Missing'), (4, 'Dormant'), (5, 'Removed')])),
                ('due_date', models.DateField(default=None, null=True)),
                ('checked_out_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department')),
                ('min_required_certs', models.ManyToManyField(to='core.Certification', verbose_name='Minimal Certifications Required for Rental')),
            ],
            options={
                'verbose_name_plural': 'Gear',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(choices=[('membership', 'membership quiz questions'), ('staffhood', 'stafhood quiz questions'), ('special', 'special questions for special purposes'), ('other', 'yeah, not sure. something else')], max_length=20)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('question_text', models.CharField(max_length=100)),
                ('error_message', models.CharField(max_length=100)),
                ('answers', models.ManyToManyField(to='core.Answer')),
                ('correct_answer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='core.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Staffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exc_email', models.EmailField(max_length=255, unique=True, verbose_name='Official ExC Email')),
                ('autobiography', models.TextField(default='I am too lazy and lame to upload a bio!', verbose_name='Self Description of the staffer')),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('Rental', (('CheckOut', 'Check Out'), ('CheckIn', 'Check In'), ('Inventory', 'In Stock'))), ('Admin Actions', (('Create', 'New Gear'), ('Delete', 'Remove Gear'), ('ReTag', 'Change Tag'), ('Break', 'Set Broken'), ('Fix', 'Set Fixed'), ('Override', 'Admin Override'))), ('Auto Updates', (('Missing', 'Gear Missing'), ('Expire', 'Gear Expiration')))], max_length=20)),
                ('comments', models.TextField(default='')),
                ('authorizer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='has_authorized', to=settings.AUTH_USER_MODEL, validators=[core.models.TransactionModels.validate_auth])),
                ('gear', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='has_checked_out', to='core.Gear', validators=[core.models.TransactionModels.validate_available])),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='stls',
            field=models.ManyToManyField(related_name='STLs_of', to='core.Staffer'),
        ),
        migrations.AddField(
            model_name='member',
            name='certifications',
            field=models.ManyToManyField(to='core.Certification'),
        ),
        migrations.AddField(
            model_name='member',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group'),
        ),
    ]
