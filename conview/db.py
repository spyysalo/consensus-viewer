from flask import current_app
from flask import g
from logging import info, error

try:
    import sqlitedict
except ImportError:
    error('failed `import sqlitedict`, try `pip3 install sqlitedict`')


def get_dbs():
    if 'dbs' not in g:
        g.dbs = []
        for dbpath in current_app.config['DATABASES']:
            info('open db {}'.format(dbpath))
            g.dbs.append(sqlitedict.SqliteDict(dbpath, flag='r'))
    return g.dbs


def close_dbs(err=None):
    if 'dbs' in g:
        info('close dbs')
        for db in g.dbs:
            db.close()
        g.pop('dbs')
    else:
        info('no dbs to close')


def init(app):
    app.teardown_appcontext(close_dbs)
