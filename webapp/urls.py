from tornado import web
from conf import settings

from apps.auth.urls import url_patterns as auth_url_patterns
from apps.api.urls import url_patterns as api_url_patterns


base_url_patterns = [
    # Websocket handlers.
    # (r'/ws', ws.WSHandler),

    # Static file handlers.
    (r'/static/(.*)', web.StaticFileHandler, {'path': settings['static_path']}),
]


url_patterns = auth_url_patterns + api_url_patterns + base_url_patterns
