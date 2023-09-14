# Generated by Django 3.2.3 on 2023-09-25 03:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClicheApp',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(
                    auto_now_add=True, db_index=True)),
                ('modified_time', models.DateTimeField(
                    auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid1, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('path', models.CharField(blank=True, max_length=511)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClicheAppDependency',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(
                    auto_now_add=True, db_index=True)),
                ('modified_time', models.DateTimeField(
                    auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(
                    default=uuid.uuid1, unique=True)),
                ('dependant', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='dependencies',
                    to='cliche_apps.clicheapp')),
                ('dependency', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='dependants',
                    to='cliche_apps.clicheapp')),
            ],
            options={
                'unique_together': {('dependant', 'dependency')},
            },
        ),
    ]