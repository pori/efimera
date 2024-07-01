from flask import Blueprint, request, jsonify

from .models import Note, Link, Tag
from .utils import save_data_to_db

bp = Blueprint('main', __name__)

@bp.route('/notes', methods=['POST'])
def parse_text():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text_blob = data['text']
    try:
        save_data_to_db(text_blob)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Data saved successfully'}), 200

@bp.route('/notes', methods=['GET'])
def get_notes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)

    query = Note.query

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(Note.text.ilike(search_pattern))

    notes_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    notes = notes_paginated.items

    result = []
    for note in notes:
        links = Link.query.filter_by(note_id=note.id).all()
        tags = Tag.query.filter_by(note_id=note.id).all()

        note_data = {
            'id': note.id,
            'text': note.text,
            'links': [{'id': link.id, 'url': link.url, 'title': link.title, 'description': link.description, 'image': link.image} for link in links],
            'tags': [{'id': tag.id, 'tag': tag.tag} for tag in tags]
        }
        result.append(note_data)

    response = {
        'notes': result,
        'total': notes_paginated.total,
        'pages': notes_paginated.pages,
        'current_page': notes_paginated.page,
        'next_page': notes_paginated.next_num,
        'prev_page': notes_paginated.prev_num
    }

    return jsonify(response)

