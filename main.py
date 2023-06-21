# authors: Nathaniel Shafran Avshalom, Dev Katyal 
# Description: backend. API. for GlobalVision App
from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, resourceurl

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#adding API routers 
app.include_router(auth.router)
app.include_router(resourceurl.router)
