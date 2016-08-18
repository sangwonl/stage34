import json


class JSONResponse(object):
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data
        self.headers = {'Content-Type': 'application/json'}

    @property
    def body(self):
        return json.dumps(self.data)

    def set_header(self, name, val):
        self.headers[name] = val


class JSENDSuccess(JSONResponse):
    def __init__(self, status_code, data):
        super(JSENDSuccess, self).__init__(status_code, {'status': 'success', 'data': data})


class JSENDFail(JSONResponse):
    def __init__(self, status_code, data):
        super(JSENDFail, self).__init__(status_code, {'status': 'fail', 'data': data})


class JSENDError(JSONResponse):
    def __init__(self, status_code, msg, code=None, data=None):
        jsend = {'status': 'error', 'message': msg}
        if code: jsend.update({'code': code})
        if data: jsend.update({'data': data})
        super(JSENDError, self).__init__(status_code, jsend)
