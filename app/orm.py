from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from .models import NoteModel, Base
from .schemas import NotePOSTSchema


def commit_and_refresh(db: Session, model: Base):
    db.commit()
    db.refresh(model)
    return model


def get_note(db: Session, id_: int):
    return db.query(NoteModel).filter(NoteModel.id == id_).first()


def get_note_list(db: Session, query: Optional[str] = None):
    if query:
        return db.query(NoteModel).filter(or_(NoteModel.title.contains(query), NoteModel.content.contains(query)))
    return db.query(NoteModel).all()


def create_note(db: Session, note: NotePOSTSchema):
    db_note = NoteModel(**note.dict())
    db.add(db_note)
    return commit_and_refresh(db, db_note)


def update_note(db: Session, note: NotePOSTSchema, id_: int):
    db_note = get_note(db, id_)
    if db_note is None:
        return db_note
    db_note.title = note.title
    db_note.content = note.content
    return commit_and_refresh(db, db_note)


def delete_note(db: Session, id_: int):
    note = get_note(db, id_)
    if note is None:
        return False
    db.delete(note)
    db.commit()
    return True
