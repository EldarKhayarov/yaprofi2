from typing import Optional, List

from fastapi import APIRouter, Depends, Response, status, Body
from sqlalchemy.orm import Session

from . import schemas, orm
from .models import NoteModel
from .database_base import SessionLocal


router = APIRouter()


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def unpack_to_schema(model: NoteModel):
    return schemas.NoteGETSchema(id=model.id, title=model.title, content=model.content)


# paths
@router.get("/notes", response_model=List[schemas.NoteGETSchema])
def note_list_get(query: Optional[str] = None, db: Session = Depends(get_db_session)):
    return [unpack_to_schema(res) for res in orm.get_note_list(db, query)]


@router.get("/notes/{note_id}", response_model=schemas.NoteGETSchema)
def note_get(note_id: int, db: Session = Depends(get_db_session)):
    note = orm.get_note(db, note_id)
    if note is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return unpack_to_schema(note)


@router.post("/notes", response_model=schemas.NoteGETSchema, status_code=status.HTTP_201_CREATED)
def note_post(note: schemas.NotePOSTSchema = Body(...), db: Session = Depends(get_db_session)):
    return unpack_to_schema(orm.create_note(db, note))


@router.put("/notes/{note_id}", response_model=schemas.NoteGETSchema)
def note_put(note_id: int, note_request: schemas.NotePOSTSchema = Body(...), db: Session = Depends(get_db_session)):
    note_response = orm.update_note(db, note_request, note_id)
    if note_response is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return unpack_to_schema(note_response)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def note_delete(note_id: int, db: Session = Depends(get_db_session)):
    has_deleted = orm.delete_note(db, note_id)
    if not has_deleted:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
