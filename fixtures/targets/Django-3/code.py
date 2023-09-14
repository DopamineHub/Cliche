import os
import pathlib
import re

global project

target = 'Django-3'

files = {
    'manage.py': '\n'.join([
        '#!/usr/bin/env python',
        '"""Django\'s command-line utility for administrative tasks."""',
        'import os',
        'import sys',
        '',
        '',
        'def main():',
        '    """Run administrative tasks."""',
        '    os.environ.setdefault(\'DJANGO_SETTINGS_MODULE\', \'settings\')',
        '    try:',
        '        from django.core.management import execute_from_command_line',
        '    except ImportError as exc:',
        '        raise ImportError(',
        '           "Couldn\'t import Django. Are you sure it\'s installed and "',
        '           "available on your PYTHONPATH environment variable? Did you "',
        '           "forget to activate a virtual environment?"',
        '        ) from exc',
        '    execute_from_command_line(sys.argv)',
        '',
        '',
        'if __name__ == \'__main__\':',
        '    main()',
        '',
    ]),
    'asgi.py': '\n'.join([
        '"""',
        'ASGI config for project.',
        '',
        'For more information on this file, see',
        'https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/',
        '"""',
        '',
        'import os',
        '',
        'from django.core.asgi import get_asgi_application',
        '',
        'os.environ.setdefault(\'DJANGO_SETTINGS_MODULE\', \'settings\')',
        '',
        'application = get_asgi_application()',
        '',
    ]),
    'wsgi.py': '\n'.join([
        '"""',
        'WSGI config for project.',
        '',
        'For more information on this file, see',
        'https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/',
        '"""',
        '',
        'import os',
        '',
        'from django.core.wsgi import get_wsgi_application',
        '',
        'os.environ.setdefault(\'DJANGO_SETTINGS_MODULE\', \'settings\')',
        '',
        'application = get_wsgi_application()',
        '',
    ])
}


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def build_proj(proj):
    # create repo dir ------------------------------------------
    proj_dir = os.path.join(proj['directory'], proj['name'])
    proj_dir = pathlib.Path(proj_dir)
    proj_dir = proj_dir.resolve()
    proj_dir.mkdir(parents=True, exist_ok=True)

    # create requirements --------------------------------------
    proj_requirements = proj['requirements']
    with open(proj_dir / 'requirements.txt', 'w') as f:
        assert isinstance(proj_requirements, dict)
        for name, version in proj_requirements.items():
            f.write(f'{name}=={version}\n')

    # create manage.py -----------------------------------------
    with open(proj_dir / 'manage.py', 'w') as f:
        f.write(files['manage.py'])

    # create apps dirs -----------------------------------------
    apps_dir = proj_dir / 'apps'
    apps_dir.mkdir(parents=True, exist_ok=True)
    (apps_dir / '__init__.py').touch(exist_ok=True)

    proj_scripts = proj['scripts']
    build_script(apps_dir / 'scripts.py', proj_scripts)

    proj_apps = proj['apps']
    for app in proj_apps:
        # create app dir
        app_dir = apps_dir / app.name
        app_dir.mkdir(parents=True, exist_ok=True)
        (app_dir / '__init__.py').touch(exist_ok=True)
        build_app(app_dir, app, proj_scripts)

    # create settings dir --------------------------------------
    settings_dir = proj_dir / 'settings'
    settings_dir.mkdir(parents=True, exist_ok=True)
    # (settings_dir / '__init__.py').touch(exist_ok=True)

    # create settings/__init__.py ------------------------------
    proj_settings = proj['settings']
    build_setting(
        settings_dir / '__init__.py', proj_apps, proj_settings)
    # create urls.py -------------------------------------------
    build_setting_url(settings_dir / 'urls.py', proj_apps)

    # create wsgi.py -------------------------------------------
    with open(settings_dir / 'wsgi.py', 'w+') as f:
        f.write(files['wsgi.py'])

    # create asgi.py -------------------------------------------
    with open(settings_dir / 'asgi.py', 'w+') as f:
        f.write(files['asgi.py'])


def build_setting(path, apps, settings):
    assert isinstance(settings, dict)
    settings.setdefault(
        'SECRET_KEY',
        'django-insecure-b&tun9)kj=gb(eb+zgh4*8zf!=cxb0&b*de7a=@^600_h++690'
    )
    settings.setdefault('DEBUG', True)
    settings.setdefault('LANGUAGE_CODE', 'en-us')
    settings.setdefault('TIME_ZONE', 'UTC')
    settings.setdefault('USE_I18N', True)
    settings.setdefault('USE_L10N', True)
    settings.setdefault('USE_TZ', True)
    settings.setdefault('STATIC_URL', '/static/')
    settings.setdefault('STATIC_ROOT', '.static/')
    settings.setdefault('MEDIA_URL', '/media/')
    settings.setdefault('MEDIA_ROOT', '.media/')

    lines = [
        'from pathlib import Path',
        '',
        '',
        'BASE_DIR = Path(__file__).resolve().parent.parent',
        '',
        '',
    ]

    # write INSTALLED_APPS ----------------------------------
    setting_installed_apps = settings.pop('INSTALLED_APPS', [])
    assert isinstance(setting_installed_apps, list)
    setting_installed_apps = set(setting_installed_apps)
    setting_local_apps = [f'apps.{app.name}' for app in apps]
    lines.append('INSTALLED_APPS = [')
    lines.extend([
        f'    \'{name}\',' for
        name in setting_installed_apps.difference(setting_local_apps)
    ])
    lines.extend([
        f'    \'{name}\',' for
        name in setting_local_apps
    ])
    lines.extend([']', ''])

    # write MIDDLEWARE --------------------------------------
    setting_middleware = settings.pop('MIDDLEWARE', [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ])
    assert isinstance(setting_middleware, list)
    lines.append('MIDDLEWARE = [')
    lines.extend([f'    \'{name}\',' for name in setting_middleware])
    lines.extend([']', ''])

    # write TEMPLATES ----------------------------------------
    setting_templates = settings.pop('TEMPLATES', [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }])
    assert isinstance(setting_templates, list)
    lines.extend([f'TEMPLATES = {setting_templates}', ''])

    # write ROOT_URLCONF -------------------------------------
    settings.pop('ROOT_URLCONF', None)  # can not change ROOT_URLCONF
    lines.extend(['ROOT_URLCONF = \'settings.urls\'', ''])

    # write WSGI_APPLICATION ---------------------------------
    settings.pop('WSGI_APPLICATION', None)  # can not change WSGI_APPLICATION
    lines.extend(['WSGI_APPLICATION = \'settings.wsgi.application\'', ''])

    # write DATABASES ----------------------------------------
    setting_databases = settings.pop('DATABASES', {
        'default': {
            'ATOMIC_REQUESTS': True,
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    })
    assert isinstance(setting_databases, dict)
    lines.extend([f'DATABASES = {setting_databases}', ''])

    for name, value in settings.items():
        value = f'\'{value}\'' if isinstance(value, str) else str(value)
        lines.extend([f'{name} = {value}', ''])

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_setting_url(path, apps):
    lines = [
        'from django.urls import include, path',
        '',
        '',
        'urlpatterns = [',
    ]
    lines.extend([
        f'    path(\'{app.path}\', '
        f'include(\'apps.{app.name}.urls\')),'
        for app in apps
    ])
    lines.extend([']', ''])

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_script(path, scripts):
    lines = []
    line_imports = set()
    for script in scripts:
        for v, m in script.imports.items():
            line_imports.add(f'from {m} import {v}')
    line_imports = list(line_imports)
    line_imports.sort()

    # add imports lines
    lines.extend(line_imports)

    for script in scripts:
        script_params = ', '.join(
            f'{k}: {v}' for k, v in script.parameters.items())
        script_define = f'def {script.name}({script_params}):'
        lines.extend([
            '',
            '',
            script_define,
            f'    """ {script.description} """'
        ])
        lines.extend([
            f'    {ln}' for ln in script.code.split('\n')
        ])

    lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_app(path, app, scripts):
    # build migration ------------------------------------------
    migration_dir = path / 'migrations'
    migration_dir.mkdir(parents=True, exist_ok=True)
    (migration_dir / '__init__.py').touch(exist_ok=True)

    # build app config -----------------------------------------
    build_app_config(path / 'apps.py', app)

    # build admin ----------------------------------------------
    build_app_admin(path / 'admin.py', app)

    # build models ---------------------------------------------
    build_app_model(path / 'models.py', app)

    # build schemas --------------------------------------------
    build_app_schema(path / 'schemas.py', app)

    # build scripts --------------------------------------------
    build_app_script(path / 'scripts.py', app)

    # build views ----------------------------------------------
    build_app_view(path / 'views.py', app, scripts)

    # build urls -----------------------------------------------
    build_app_url(path / 'urls.py', app)


def build_app_config(path, app):
    lines = [
        'from django.apps import AppConfig as _AppConfig',
        '',
        '',
        'class AppConfig(_AppConfig):',
        '    default_auto_field = \'django.db.models.BigAutoField\'',
        f'    name = \'apps.{app.name}\'',
        f'    label = \'{app.name}\'',
        '',
    ]

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_app_admin(path, app):
    models = list(app.models.all())
    lines = [
        'from django.contrib import admin',
    ]
    lines.extend([
        f'from .models import {model.name}' for
        model in models
    ])
    lines.extend(['', ''])
    lines.extend([
        f'admin.site.register({model.name})' for
        model in models
    ])
    lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_app_model(path, app):
    models = list(app.models.all())
    lines = [
        'from django.db import models',
    ]

    for model in models:
        lines.extend([
            '',
            '',
            f'class {model.name}(models.Model):',
            f'    """ {model.description} """',
        ])
        model_fields = list(
            model.fields.select_related(
                'type',
                'model_foreign',
                'model_foreign__app',
            ).all()
        )
        for field in model_fields:
            field_attrs = {
                name: v['default'] for name, v in
                field.type.attributes.items()
            }
            field_attrs.update(field.attributes)
            lines.extend([
                '',
                f'    # {field.description}',
                f'    {field.name} = models.{field.type_id}Field(',
            ])
            if field.type_id == 'ForeignKey':
                model_foreign = field.model_foreign
                lines.append(
                    f'        \'{model_foreign.app.name}:'
                    f'{model_foreign.name}\','
                )

            lines.extend([
                f'        {k}={v},'
                for k, v in field_attrs.items()
            ])
            lines.extend([
                '    )',
            ])

        model_attrs = {
            k: str(v)
            for k, v in model.attributes.items()
        }
        model_attrs.setdefault(
            'db_table', f'\'{camel_to_snake(model.name)}\'')
        lines.extend([
            '',
            '    class Meta:',
        ])
        lines.extend([
            f'        {k} = {v}' for
            k, v in model_attrs.items()
        ])

    lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_app_schema(path, app):
    field_attrs_mapping = {
        'source': 'data_key',
        'null': 'allow_none',
        'read_only': 'dump_only',
        'write_only': 'load_only',
        'default': 'missing',
    }
    field_attrs_ex_mapping = {
        'max_value': {'validate.Range': 'max'},
        'min_value': {'validate.Range': 'max'},
        'max_length': {'validate.Length': 'max'},
        'min_length': {'validate.Length': 'min'},
    }

    schemas = list(app.schemas.all())
    lines = [
        'from marshmallow import Schema, fields, validate',
    ]

    for schema in schemas:
        lines.extend([
            '',
            '',
            f'class {schema.name}(Schema):',
            f'    """ {schema.description} """',
        ])

        schema_fields = list(
            schema.fields.select_related(
                'type',
                'schema_nested',
                'schema_nested__app',
            ).all()
        )
        for field in schema_fields:
            field_attrs_origin = {
                name: v['default'] for name, v in
                field.type.attributes.items()
            }
            field_attrs_origin.update(field.attributes)
            field_attrs = {
                field_attrs_mapping.get(k) or k: v
                for k, v in field_attrs_origin.items()
                if k not in field_attrs_ex_mapping
            }
            field_attrs_ex = {}
            for k, v in field_attrs_origin.items():
                if v is None:
                    continue

                k_ = field_attrs_ex_mapping.get(k)
                if not isinstance(k_, dict):
                    continue

                for k_k, k_v in k_.items():
                    field_attrs_ex.setdefault(
                        k_k, {}).update({k_v: v})

            lines.extend([
                '',
                f'    # {field.description}',
                f'    {field.name} = fields.{field.type_id}(',
            ])
            if field.type_id == 'Nested':
                schema_nested = field.schema_nested
                lines.append(
                    f'        \'{schema_nested.name}\','
                )
            lines.extend([
                f'        {k}={v},'
                for k, v in field_attrs.items()
            ])
            if field_attrs_ex:
                lines.append('        validate=[')
                for v_func, v_values in field_attrs_ex.items():
                    lines.append(f'            {v_func}(')
                    for k, v in v_values.items():
                        lines.append(f'                {k}={v},')
                    lines.append('            ),')
                lines.append('        ],')
            lines.extend([
                '    )',
            ])

    lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_app_script(path, app):
    build_script(path, list(app.scripts.all()))


def build_app_view(path, app, scripts):
    views = list(app.views.all())
    schemas = list(app.schemas.all())
    scripts_local = list(app.scripts.all())
    lines = [
        'from django.apps import apps',
        'from django.core import exceptions',
        'from django import http',
        'from django import shortcuts',
        'from django import views',
        '',
    ]
    lines.extend([
        f'from ..scripts import {s.name}' for
        s in scripts
    ])
    lines.extend([
        f'from .scripts import {s.name}' for
        s in scripts_local
    ])
    lines.extend([
        f'from .schemas import {s.name}' for
        s in schemas
    ])
    for view in views:
        lines.extend([
            '',
            '',
            f'class {view.name}(views.View):',
            f'    """ {view.description} """',
        ])
        for method in view.methods.select_related(
                'model',
                'model__app',
                'filter_schema',
                'input_schema',
                'output_schema',
        ).all():
            method_params = 'self, request, *args, **kwargs'
            method_define = f'def {method.type.lower()}({method_params}):'
            method_options = {
                'model': (
                    f'apps.get_model('
                    f'\'{method.model.app.name}.{method.model.name}\''
                    f')' if method.model else 'None'
                ),
                'filter_schema': (
                    f'{method.filter_schema.name}()'
                    if method.filter_schema else 'None'
                ),
                'input_schema': (
                    f'{method.input_schema.name}()'
                    if method.input_schema else 'None'
                ),
                'output_schema': (
                    f'{method.output_schema.name}()'
                    if method.output_schema else 'None'
                ),
                'path_args': 'kwargs',
            }
            lines.extend([
                '',
                f'    {method_define}',
                f'        """ {method.description} """',
            ])
            scripts = list(method.scripts.filter(
                target=target
            ).select_related('script').all())
            for script in scripts:
                script_name = script.script.name
                lines.append(
                    f'        return {script_name}(request, dict('
                )
                lines.extend([
                    f'            {k}={v},'
                    for k, v in method_options.items()
                ])
                lines.append('        ))')

            if not scripts:
                lines.append(
                    '        raise exceptions.RequestAborted('
                    '\'not implemented yet\')'
                )

    lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def build_app_url(path, app):
    views = list(app.views.all())
    lines = [
        'from django.urls import path',
    ]
    lines.extend([
        f'from .views import {view.name}'
        for view in views
    ])
    lines.extend([
        '',
        '',
        f'app_name = \'{app.name}\'',
        '',
        '',
        'urlpatterns = [',
    ])
    lines.extend([
        f'    path(\'{view.path}\', {view.name}.as_view()),'
        for view in views
    ])
    lines.extend([']', ''])

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


# start build project
build_proj(project)  # noqa
