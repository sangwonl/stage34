from sqlalchemy_wrapper import SQLAlchemy
from conf import settings


db_conn = None


def _create_sqlalchemy_db(engine, dbname, host=None, port=None, user=None, pw=None, metadata=None):
    credentials = '%s:%s' % (user, pw) if user else ''
    host_port = '@%s:%s' % (host, str(port)) if host else ''
    def_dbname = '/%s' % dbname if dbname else ''
    db_uri = '%s://%s%s%s' % (engine, credentials, host_port, def_dbname)
    return SQLAlchemy(db_uri, metadata=metadata)


def get_sqlalchemy_db(metadata=None):
    global db_conn
    if not db_conn:
        db_cfg = settings['database'].copy()
        db_cfg.update({'metadata': metadata})
        db_conn = _create_sqlalchemy_db(**db_cfg)
    return db_conn
