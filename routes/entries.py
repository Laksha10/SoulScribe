from flask import Blueprint, request, jsonify
from db.connection import db
from db.models import JournalEntry

entries_bp = Blueprint('entries', __name__, url_prefix='/entries')

# GET all entries
@entries_bp.route('/', methods=['GET'])
def get_entries():
    entries = JournalEntry.query.all()
    return jsonify([{
        'id': entry.id,
        'text': entry.text,
        'emotion': entry.emotion
    } for entry in entries])

# GET entry by ID
@entries_bp.route('/<int:id>', methods=['GET'])
def get_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    return jsonify({
        'id': entry.id,
        'text': entry.text,
        'emotion': entry.emotion
    })

# POST a new entry
@entries_bp.route('/', methods=['POST'])
def add_entry():
    data = request.get_json()
    new_entry = JournalEntry(text=data['text'], emotion=data['emotion'])
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Entry created successfully'}), 201

# PUT (update) an entry by ID
@entries_bp.route('/<int:id>', methods=['PUT'])
def update_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    data = request.get_json()
    entry.text = data.get('text', entry.text)
    entry.emotion = data.get('emotion', entry.emotion)
    db.session.commit()
    return jsonify({'message': 'Entry updated successfully'})

# DELETE an entry by ID
@entries_bp.route('/<int:id>', methods=['DELETE'])
def delete_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Entry deleted successfully'})
