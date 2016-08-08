from tornado import autoreload
from tornado import httpserver
from tornado import ioloop
from tornado import web

from conf import settings
from urls import url_patterns

import signal
import time
import tcelery
import logging


class TornadoApplication(web.Application):
    def __init__(self, env='local', io_loop=None, **kwargs):
        # initialize tornado application..
        web.Application.__init__(self, url_patterns, **settings)

        # initialize logger..
        logging.basicConfig()
        self.logger = logging.getLogger('APP')
        self.logger.setLevel(logging.DEBUG)

        # internal variables..
        self.env = env
        self.http_srv = None
        self.io_loop = io_loop or ioloop.IOLoop.instance()

        # setup services..
        self.setup_services()

    def setup_services(self):
        # configs per environment..
        # env_cfgs = self.settings

        # setup celery nonblocking producer..
        # tcelery.setup_nonblocking_producer(io_loop=self.io_loop)
        pass

    def start(self, host='0.0.0.0', port=8000):
        # register system signam handlers..
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        # tornado http server..
        self.http_srv = httpserver.HTTPServer(self)
        self.http_srv.listen(port)
        self.logger.info('Tornado server starts successfully..')
        self.logger.info('Listening to %d..' % port)

        # autoload setup and start io loop..
        autoreload.start(self.io_loop)
        self.io_loop.start()

    def shutdown(self):
        self.http_srv.stop()

        shutdown_deadline = time.time() + 10
        def stop_loop():
            now = time.time()
            if now < shutdown_deadline and self.io_loop._callbacks:
                self.io_loop.add_timeout(now + 1, stop_loop)
            else:
                self.io_loop.stop()

        stop_loop()

    def signal_handler(self, signal_number, frame):
        ioloop.IOLoop.instance().add_callback(self.shutdown)


def main():
    import os
    env = os.environ.get('ENV', 'local')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', nargs='?', default='0.0.0.0')
    parser.add_argument('--port', nargs='?', default=8000, type=int)
    args = parser.parse_args()

    app = TornadoApplication(env)
    app.start(args.host, args.port)


if __name__ == '__main__':
    main()