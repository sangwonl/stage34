from django.http import JsonResponse


class JSENDSuccess(JsonResponse):
    def __init__(self, status_code, data={}):
        super(JSENDSuccess, self).__init__(status=status_code, data={'status': 'success', 'data': data})


class JSENDFail(JsonResponse):
    def __init__(self, status_code, data={}):
        super(JSENDFail, self).__init__(status=status_code, data={'status': 'fail', 'data': data})


class JSENDError(JsonResponse):
    def __init__(self, status_code, msg, code=None, data=None):
        content = {'status': 'error', 'message': msg}
        if code: jsend.update({'code': code})
        if data: jsend.update({'data': data})
        super(JSENDError, self).__init__(status=status_code, data=content)
