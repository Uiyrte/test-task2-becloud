from fastapi import FastAPI

from app.database import Base, engine
from app.routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks_router)
