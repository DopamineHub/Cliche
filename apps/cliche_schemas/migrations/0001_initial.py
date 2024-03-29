# Generated by Django 3.2.3 on 2023-12-07 03:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliche_apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClicheSchema',
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
                ('name', models.CharField(max_length=255)),
                ('attributes', models.JSONField(default=dict)),
                ('app', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='schemas',
                    to='cliche_apps.clicheapp')),
            ],
            options={
                'unique_together': {('app', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ClicheSchemaFieldType',
            fields=[
                ('name', models.CharField(
                    max_length=16, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('attributes', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='ClicheSchemaField',
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
                ('name', models.CharField(max_length=255)),
                ('attributes', models.JSONField(default=dict)),
                ('schema', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='fields',
                    to='cliche_schemas.clicheschema')),
                ('schema_nested', models.ForeignKey(
                    db_constraint=False, default=None, null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='nested_fields',
                    to='cliche_schemas.clicheschema')),
                ('type', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='fields',
                    to='cliche_schemas.clicheschemafieldtype')),
            ],
            options={
                'unique_together': {('schema', 'name')},
            },
        ),
    ]
