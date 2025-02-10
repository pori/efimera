from .extensions import ma
from .models import Note


class NoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Note

    id = ma.auto_field()
    text = ma.auto_field()
