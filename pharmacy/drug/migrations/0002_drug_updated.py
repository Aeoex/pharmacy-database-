# Generated by Django 5.1.3 on 2024-12-16 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
