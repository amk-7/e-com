# Generated by Django 3.2.6 on 2023-02-20 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0009_commande_issold'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='delivery',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ventes.manager'),
        ),
    ]
