# Generated by Django 3.2.6 on 2023-02-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0008_rename_cotegorie_subcategorie_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='isSold',
            field=models.BooleanField(default=False, null=True),
        ),
    ]