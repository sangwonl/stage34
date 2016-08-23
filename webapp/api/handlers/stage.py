from django.views import View
from django.conf import settings
from django.core import serializers
from django.forms import model_to_dict

from api.helpers.mixins import AuthRequiredMixin
from api.helpers.http.jsend import JSENDSuccess, JSENDError
from api.models import User

import json
import jwt


class StageRootHandler(AuthRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JSENDSuccess(status_code=200, data=[])
