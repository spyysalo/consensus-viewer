from flask import current_app
from flask import g
from logging import error

try:
    import sqlitedict
except ImportError:
    error('failed `import sqlitedict`, try `pip3 install sqlitedict`')


def get_db():
    if 'db' not in g:
        dbpath = current_app.config['DATABASE']
        error('open db {}'.format(dbpath))
        g.db = sqlitedict.SqliteDict(dbpath, flag='r')
    return g.db


def close_db(err=None):
    if 'db' in g:
        error('close db')
        g.db.close()
        g.pop('db')
    else:
        error('no db to close')


def init(app):
    app.teardown_appcontext(close_db)
