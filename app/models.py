from sqlalchemy import Column, Integer, String, Text

from .database_base import Base


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=True)
    content = Column(Text, index=True)
