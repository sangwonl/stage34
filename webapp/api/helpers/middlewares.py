from django.contrib import auth


class JWTAuthenticationMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated:
            auth_bearer = request.META.get('HTTP_AUTHORIZATION')
            if auth_bearer and 'token' in auth_bearer:
                token = auth_bearer.replace('token', '').strip()
                request.user = auth.authenticate(token=token)
