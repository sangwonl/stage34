import json


class JSONResponse(object):
    def __init__(self, status, data):
        self.status = status
        self.data = data
        self.headers = {'Content-Type': 'application/json'}

    @property
    def body(self):
        return json.dumps({'data': self.data})

    def set_header(self, name, val):
        self.headers[name] = val