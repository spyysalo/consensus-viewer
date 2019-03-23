from flask import Blueprint
from flask import Response, render_template, abort

from .db import get_dbs

bp = Blueprint('view', __name__, url_prefix='/view')


@bp.route('/')
def show_documents():
    db = get_dbs()[0]
    return str(list(db.keys()))


@bp.route('/<id_>.txt')
def show_document_text(id_):
    texts = []
    for i, db in enumerate(get_dbs()):
        if i != 0:
            texts.append('\n---\n')
        text = db.get('{}.txt'.format(id_), None)
        if text is None:
            text = '[not found]'
        texts.append(text)
    return Response('\n'.join(texts), mimetype='text/plain')


@bp.route('/<id_>.ann')
def show_document_ann(id_):
    anns = []
    for i, db in enumerate(get_dbs()):
        if i != 0:
            anns.append('\n---\n')
        ann = db.get('{}.ann'.format(id_), None)
        if ann is None:
            ann = '[not found]'
        anns.append(ann)
    return Response('\n'.join(anns), mimetype='text/plain')


def _filter_by_type(standoffs, remove):
    filtered = []
    for s in standoffs:
        try:
            fields = s.split('\t')
            type_ = fields[1].split()[0]
            if type_ in remove:
                continue
        except Exception as e:
            error(e)
        filtered.append(s)
    return filtered


@bp.route('/<id_>')
def visualize_document(id_):
    from .so2html import standoff_to_html, Standoff
    doc_id = id_
    html = ['<!DOCTYPE html>\n<html>\n<body class="clearfix">']
    for i, db in enumerate(get_dbs()):
        if i != 0:
            html.append('<hr style="margin:20px">')
        html.append('<div class="clearfix">')
        text = db.get('{}.txt'.format(doc_id), None)
        ann = db.get('{}.ann'.format(doc_id), None)
        if text is None and ann is None:
            text, ann = "[not found]", ""
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
        html.append(standoff_to_html(text, standoffs, tooltips=True,
                                     links=True, embeddable=True))
        html.append('</div>')
    html.append('</body>\n</html>')
    return '\n'.join(html)


@bp.route('/<id_>.brat')
def brat_visualize_document(id_):
    data = []
    doc_id = id_
    for db in get_dbs():
        text = db.get('{}.txt'.format(doc_id), None)
        ann = db.get('{}.ann'.format(doc_id), None)
        if text is None and ann is None:
            text, ann = '[not found]', ''
        filtered = []
        for a in ann.split('\n'):
            if a and a[0] in 'TN':
                filtered.append(a)
        filtered = _filter_by_type(filtered, set(['Token']))
        ann = '\n'.join(filtered)
        data.append(text.replace('\n', ' ') + ann)
    return render_template('bratvis.html', data=data)
