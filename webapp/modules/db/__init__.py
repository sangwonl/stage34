from sqlalchemy_wrapper import SQLAlchemy


def create_connecter(engine, dbname, host=None, port=None, user=None, pw=None, metadata=None):
    credentials = '%s:%s' % (user, pw) if user else ''
    host_port = '@%s:%s' % (host, str(port)) if host else ''
    def_dbname = '/%s' % dbname if dbname else ''
    db_uri = '%s://%s%s%s' % (engine, credentials, host_port, def_dbname)
    return SQLAlchemy(db_uri, metadata=metadata)
