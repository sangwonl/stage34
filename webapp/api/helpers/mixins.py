from django.contrib.auth.mixins import LoginRequiredMixin


class AuthRequiredMixin(LoginRequiredMixin):
    permission_denied_message = 'Authentication Failed'
    raise_exception = True
