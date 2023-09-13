from django.db import models


def patch():
    # path to meet demand of Ctrip DBA
    # models.CharField = CharField
    # models.TextField = TextField
    models.OneToOneField = OneToOneField
    models.ForeignKey = ForeignKey
    models.ManyToManyField = ManyToManyField


def patch_mysql():
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.data_types['AutoField'] = 'bigint AUTO_INCREMENT'


class CharField(models.CharField):
    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = ''
        super().__init__(*args, **kwargs)


class TextField(models.TextField):
    def __init__(self, *args, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = ''
        super().__init__(*args, **kwargs)


class OneToOneField(models.OneToOneField):
    def __init__(self, *args, **kwargs):
        # if 'default' not in kwargs:
        #     kwargs['null'] = True
        #     kwargs['default'] = None
        kwargs['db_constraint'] = False
        super().__init__(*args, **kwargs)


class ForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        # if 'default' not in kwargs:
        #     kwargs['null'] = True
        #     kwargs['default'] = None
        kwargs['db_constraint'] = False
        super().__init__(*args, **kwargs)


class ManyToManyField(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        if 'through' not in kwargs:
            kwargs['db_constraint'] = False
        super().__init__(*args, **kwargs)
