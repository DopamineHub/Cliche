# Generated by Django 3.2.3 on 2023-12-07 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliche_schemas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clicheschema',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clicheschemafield',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
