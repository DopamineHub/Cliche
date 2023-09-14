from http import HTTPStatus
from django.http import HttpRequest
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.models.base import ModelBase
from marshmallow import Schema
from marshmallow.exceptions import ValidationError


def model_view_create(request: HttpRequest, options: dict):
    """ desc: create model instance """
    """ uuid: 0054630a-ac47-11ee-b0c9-ba4b1618bd02 """
    model = options.get('model')
    if not isinstance(model, ModelBase):
        raise AssertionError('model not provided')

    schema = options.get('intput_schema')
    if not isinstance(schema, Schema):
        raise AssertionError('input schema not provided')

    try:
        input_args = schema.loads(request.body)
    except ValidationError:
        return JsonResponse({
            'error': 'Invalid Data'}, status=HTTPStatus.BAD_REQUEST)

    try:
        model_instance = model(**input_args)
        model_instance.save()
    except DatabaseError:
        return JsonResponse({
            'error': 'Failed to Create'}, status=HTTPStatus.CONFLICT)

    schema = options.get('output_schema')
    if not isinstance(schema, Schema):
        raise AssertionError('output schema not provided')

    return JsonResponse(schema.dumps(model_instance))


def model_view_update(request: HttpRequest, options: dict):
    """ desc: update model instance """
    """ uuid: 01ff390a-ac47-11ee-b0c9-ba4b1618bd02 """
    return JsonResponse({})


def model_view_list(request: HttpRequest, options: dict):
    """ desc: list model instance """
    """ uuid: 025485e0-ac47-11ee-b0c9-ba4b1618bd02 """
    model = options.get('model')
    if not isinstance(model, ModelBase):
        raise AssertionError('model not provided')

    arg_offset = options.get('offset') or 0
    arg_limit = options.get('limit') or 100

    model_qs = model.objects.all()
    schema = options.get('filter_schema')
    if isinstance(schema, Schema):
        filter_args = schema.load({
            k: v for k, v in request.GET.items()})
        arg_offset = filter_args.pop('offset', arg_offset)
        arg_limit = filter_args.pop('limit', arg_limit)
        model_qs = model_qs.filter(filter_args)

    schema = options.get('output_schema')
    if not isinstance(schema, Schema):
        raise AssertionError('output schema not provided')

    return JsonResponse({
        'total': model_qs.count(),
        'results': schema.dumps(
            model_qs.all()[arg_offset: arg_limit],
            many=True,
        )
    })


def model_view_retrieve(request: HttpRequest, options: dict):
    """ desc: retrieve model instance """
    """ uuid: 02bef150-ac47-11ee-b0c9-ba4b1618bd02 """
    model = options.get('model')
    if not isinstance(model, ModelBase):
        raise AssertionError('model not provided')

    model_qs = model.objects.all()
    schema = options.get('filter_schema')
    if isinstance(schema, Schema):
        model_qs = model_qs.filter(schema.load({
            k: v for k, v in request.GET.items()}))

    args = options.get('path_args')
    if not isinstance(args, dict):
        raise AssertionError('path args not provided')

    try:
        model_instance = model_qs.filter(args).get()

    except (
            ObjectDoesNotExist,
            MultipleObjectsReturned,
    ):
        return JsonResponse({
            'error': 'NotFound'}, status=HTTPStatus.NOT_FOUND)

    schema = options.get('output_schema')
    if not isinstance(schema, Schema):
        raise AssertionError('output schema not provided')

    return JsonResponse(schema.dumps(model_instance))


def model_view_destroy(request: HttpRequest, options: dict):
    """ desc: destroy model instance """
    """ uuid: 1a791f1e-ac47-11ee-b0c9-ba4b1618bd02 """
    return JsonResponse({})
