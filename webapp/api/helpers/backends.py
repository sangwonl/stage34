from django.contrib.auth import get_user_model
from django.conf import settings

import jwt


User = get_user_model()


class JWTAuthenticationBackend(object):
    def authenticate(self, token):
        try:
            payload = jwt.decode(token, key=settings.JWT_SECRET)
        except jwt.InvalidTokenError:
            return None

        uid = payload.get('uid')
        email = payload.get('email')

        try:
            user = User.objects.get(id=uid, email=email)
            user.jwt_payload = payload
        except User.DoesNotExist:
            return None

        return user

    def get_user(self, uid):
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return None
        return user
