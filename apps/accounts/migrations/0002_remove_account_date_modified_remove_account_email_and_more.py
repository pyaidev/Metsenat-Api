# Generated by Django 4.1.3 on 2023-03-01 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='date_modified',
        ),
        migrations.RemoveField(
            model_name='account',
            name='email',
        ),
        migrations.AddField(
            model_name='account',
            name='date_login',
            field=models.DateTimeField(auto_now=True, verbose_name='Yangilangan sanasi'),
        ),
        migrations.AddField(
            model_name='account',
            name='is_legal_entity',
            field=models.BooleanField(default=False, verbose_name='Yuridik shaxs'),
        ),
        migrations.AddField(
            model_name='account',
            name='is_physical_person',
            field=models.BooleanField(default=False, verbose_name='Jismoniy shaxs'),
        ),
        migrations.AddField(
            model_name='account',
            name='is_sponsor',
            field=models.BooleanField(default=False, verbose_name='Sponsor'),
        ),
        migrations.AddField(
            model_name='account',
            name='is_student',
            field=models.BooleanField(default=False, verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='account',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sanasi'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Admin'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='Superuser'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(default=1, max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Faqat O`zbekiston mobil raqamlari tasdiqlanadi('+' belgisiz!)!", regex='^998[0-9]{2}[0-9]{7}$')], verbose_name='Telefon raqam'),
            preserve_default=False,
        ),
    ]
