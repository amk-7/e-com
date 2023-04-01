# Generated by Django 3.2.6 on 2023-01-23 12:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('loveNumber', models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('media', models.FileField(upload_to='postes')),
            ],
        ),
    ]
