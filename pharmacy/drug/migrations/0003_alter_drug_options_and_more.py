# Generated by Django 5.1.3 on 2024-12-16 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug', '0002_drug_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drug',
            options={'ordering': ['name'], 'verbose_name': 'Drug', 'verbose_name_plural': 'Drugs'},
        ),
        migrations.RemoveConstraint(
            model_name='drug',
            name='unique_drug_constraint',
        ),
        migrations.RenameField(
            model_name='drug',
            old_name='drug_brand',
            new_name='brand',
        ),
        migrations.RenameField(
            model_name='drug',
            old_name='drug_dosage_unit',
            new_name='dosage_unit',
        ),
        migrations.RenameField(
            model_name='drug',
            old_name='drug_dosage_value',
            new_name='dosage_value',
        ),
        migrations.RenameField(
            model_name='drug',
            old_name='drug_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='drug',
            old_name='drug_price',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='drug',
            old_name='drug_quantity',
            new_name='quantity',
        ),
        migrations.AddConstraint(
            model_name='drug',
            constraint=models.UniqueConstraint(fields=('name', 'dosage_value', 'dosage_unit', 'brand'), name='unique_drug_constraint'),
        ),
    ]
