from importlib import import_module

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_cas_ng.utils import get_user_from_session
from rest_framework import authentication, exceptions

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class SessionAuthentication(authentication.SessionAuthentication):
    def authenticate_header(self, request):
        return 'Session'


class BearerAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _(
                'Invalid token header. '
                'Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. '
                'Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    @staticmethod
    def authenticate_credentials(key):
        session = SessionStore(session_key=key)
        user = get_user_from_session(session)
        return user, key

    def authenticate_header(self, request):
        return self.keyword
