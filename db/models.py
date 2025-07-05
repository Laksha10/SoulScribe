# db/models.py

from db.connection import db
from datetime import datetime

class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    predicted_emotions = db.Column(db.Text, nullable=False)  # Can store as comma-separated values
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<JournalEntry {self.id} - Emotions: {self.predicted_emotions}>'
