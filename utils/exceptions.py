from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import (
    exceptions,
    response,
    views,
)


class ExceptionHandler(object):
    field_code = 'error'
    field_description = 'error_description'

    def parse_as_error_detail(self, exec_detail):
        return {
            self.field_description: exec_detail,
            self.field_code: exec_detail.code,
        }

    def parse_as_list(self, exec_detail):
        details = [
            self.parse_as_any(d) for
            d in exec_detail if d
        ]
        return details[0] if len(details) == 1 else {
            self.field_description: details,
            self.field_code: 'multiple errors'
        }

    def parse_as_dict(self, exec_detail):
        details = [
            (k, self.parse_as_any(d)) for
            k, d in exec_detail.items() if d
        ]
        return {
            self.field_description: details[0][1],
            self.field_code: details[0][0]
        } if len(details) == 1 else {
            self.field_description: [
                {
                    self.field_description: v[1],
                    self.field_code: v[0],
                } for v in details
            ],
            self.field_code: 'multiple errors'
        }

    def parse_as_any(self, exec_detail):
        if isinstance(exec_detail, exceptions.ErrorDetail):
            return self.parse_as_error_detail(exec_detail)

        if isinstance(exec_detail, list):
            return self.parse_as_list(exec_detail)

        if isinstance(exec_detail, dict):
            return self.parse_as_dict(exec_detail)

        if isinstance(exec_detail, str):
            return exec_detail

        return None

    def parse(self, exec_detail):
        return self.parse_as_any(exec_detail)

    def response(self, **kwargs):
        return response.Response(**kwargs)

    def __call__(self, exc, context):
        if isinstance(exc, Http404):
            exc = exceptions.NotFound()
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()

        if isinstance(exc, exceptions.APIException):
            headers = {}

            exec_auth_header = getattr(exc, 'auth_header', None)
            if exec_auth_header:
                headers['WWW-Authenticate'] = exec_auth_header

            exec_wait = getattr(exc, 'wait', None)
            if exec_wait:
                headers['Retry-After'] = '%d' % exec_wait

            views.set_rollback()

            return self.response(
                data=self.parse(exc.detail),
                status=exc.status_code,
                headers=headers,
            )

        return None


exception_handler = ExceptionHandler()
