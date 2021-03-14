from fastapi import FastAPI

from . import routes
from .models import Base
from .database_base import engine


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(routes.router)
