from typing import Optional

from pydantic import BaseModel

from . import config


class NotePOSTSchema(BaseModel):
    title: Optional[str]
    content: str


class NoteGETSchema(NotePOSTSchema):
    id: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.title is None:
            self.title = self.content[:config.TITLE_N_FIRST_CHARS]
