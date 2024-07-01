import uuid

from sqlalchemy.dialects.postgresql import UUID

from .extensions import db


class Note(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = db.Column(db.Text, nullable=False)
    links = db.relationship('Link', backref='note', lazy=True)
    tags = db.relationship('Tag', backref='note', lazy=True)


class Link(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(512))
    description = db.Column(db.Text)
    image = db.Column(db.String(512))
    note_id = db.Column(UUID(as_uuid=True), db.ForeignKey('note.id'), nullable=False)


class Tag(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag = db.Column(db.String(), nullable=False)
    note_id = db.Column(UUID(as_uuid=True), db.ForeignKey('note.id'), nullable=False)
