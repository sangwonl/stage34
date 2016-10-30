from django.conf import settings

import os


class LogBucket(object):
    def __init__(self, name):
        self.log_path = os.path.join(settings.STAGE_REPO_HOME, name, 'output.log')
        self.logs = []
    
    def put(self, log_message, header=False):
        if header:
            log_message = '\n' + log_message
        self.logs.append(log_message)

    def flush(self):
        full_log = '\n'.join(self.logs)
        try:
            f = open(self.log_path, 'wt')
            f.write(full_log)
        except IOError:
            pass
