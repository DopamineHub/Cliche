# Generated by Django 3.2.3 on 2024-01-01 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliche_scripts', '0001_initial'),
        ('cliche_builders', '0001_initial'),
        ('cliche_views', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clicheviewmethodscript',
            unique_together={('method', 'target', 'script')},
        ),
    ]
