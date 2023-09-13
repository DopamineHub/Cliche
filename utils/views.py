from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
# from django.views.decorators import csrf
from rest_framework import (
    exceptions,
    response,
    views,
)

from .serializers import (
    UserLoginSerializer,
    UserSelfSerializer,
)


class UserLoginView(views.APIView):
    """
    user login api
    """

    permission_classes = ()

    def post(self, request, *args, **kwargs):
        ser = UserLoginSerializer(
            data=request.data,
            context=self.get_renderer_context())
        ser.is_valid(raise_exception=True)
        ser_data = ser.save()

        # authenticate user
        user = authenticate(
            request,
            username=ser_data['username'],
            password=ser_data['password'],
        )
        if not user or not user.is_active:
            raise exceptions.AuthenticationFailed('fail to login')

        # login user
        login(request, user)

        if not request.session.session_key:
            request.session.create()

        ser_data.update(
            access_token=request.session.session_key)

        ser = UserLoginSerializer(
            instance=ser_data,
            context=self.get_renderer_context(),
        )
        return response.Response(ser.data)


class UserLogoutView(views.APIView):
    """
    user logout api
    """

    def post(self, request, *args, **kwargs):
        logout(request)
        return response.Response()


class UserSelfView(views.APIView):
    """
    user self api
    """

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise exceptions.NotAuthenticated('anonymous user')

        ser = UserSelfSerializer(
            instance={
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
            },
            context=self.get_renderer_context()
        )
        return response.Response(ser.data)
