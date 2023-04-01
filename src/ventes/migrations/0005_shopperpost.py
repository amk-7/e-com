# Generated by Django 3.2.6 on 2023-01-23 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('postes', '0001_initial'),
        ('ventes', '0004_alter_shopperarticle_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopperPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postes.post')),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventes.shopper')),
            ],
        ),
    ]