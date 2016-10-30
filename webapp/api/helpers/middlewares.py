from django.contrib import auth
from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject


class JWTAuthenticationMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            auth_bearer = request.META.get('HTTP_AUTHORIZATION')
            if auth_bearer and 'token' in auth_bearer:
                token = auth_bearer.replace('token', '').strip()
                request.user = auth.authenticate(token=token)
            else:
                request.user = SimpleLazyObject(lambda: get_user(request))
