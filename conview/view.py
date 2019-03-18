from flask import Blueprint
from flask import abort

from .db import get_db

bp = Blueprint('view', __name__, url_prefix='/view')


@bp.route('/')
def show_documents():
    db = get_db()
    return str(list(db.keys()))


@bp.route('/<id_>.txt')
def show_document_text(id_):
    db = get_db()
    text = db.get('{}.txt'.format(id_), None)
    if text is None:
        abort(404)
    return text


@bp.route('/<id_>.ann')
def show_document_ann(id_):
    db = get_db()
    ann = db.get('{}.ann'.format(id_), None)
    if ann is None:
        abort(404)
    return ann


@bp.route('/<id_>')
def visualize_document(id_):
    from .so2html import standoff_to_html, Standoff
    db = get_db()
    text = db.get('{}.txt'.format(id_), None)
    ann = db.get('{}.ann'.format(id_), None)
    if text is None or ann is None:
        abort(404)
    standoffs = []
    for a in ann.split('\n'):
        if not a or a[0] != 'T':
            continue
        fields = a.split('\t')
        id_, type_start_end, ann_text = fields
        type_, start, end = type_start_end.split(' ')
        if type_ == 'Token':
            continue
        norm = 'GO:0071159'    # test, fake it
        standoffs.append(Standoff(int(start), int(end), type_, norm))
    return standoff_to_html(text, standoffs, tooltips=True, links=True)
