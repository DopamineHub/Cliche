# Generated by Django 3.2.3 on 2023-11-30 09:18

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
            name='ClicheModel',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(
                    auto_now_add=True, db_index=True)),
                ('modified_time', models.DateTimeField(
                    auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid1, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('attributes', models.JSONField(blank=True, default=dict)),
                ('app', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='models',
                    to='cliche_apps.clicheapp')),
            ],
            options={
                'unique_together': {('app', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ClicheModelFieldType',
            fields=[
                ('name', models.CharField(
                    max_length=16, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('attributes', models.JSONField(
                    blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='ClicheModelField',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(
                    auto_now_add=True, db_index=True)),
                ('modified_time', models.DateTimeField(
                    auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid1, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('attributes', models.JSONField(blank=True, default=dict)),
                ('model', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='fields',
                    to='cliche_models.clichemodel')),
                ('model_foreign', models.ForeignKey(
                    blank=True, db_constraint=False,
                    default=None, null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='foreign_fields',
                    to='cliche_models.clichemodel')),
                ('type', models.ForeignKey(
                    db_constraint=False,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='fields',
                    to='cliche_models.clichemodelfieldtype')),
            ],
            options={
                'unique_together': {('model', 'name')},
            },
        ),
    ]
