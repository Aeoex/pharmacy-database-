# Generated by Django 5.1.3 on 2024-12-16 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharma', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pharmacy',
            options={'ordering': ['name'], 'verbose_name': 'Pharmacy', 'verbose_name_plural': 'Pharmacies'},
        ),
        migrations.RenameField(
            model_name='pharmacy',
            old_name='pharmacy_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='pharmacy',
            old_name='pharmacy_name',
            new_name='name',
        ),
    ]