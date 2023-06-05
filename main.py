import models
from database import engine
from routers import auth, resourceurl
from fastapi import FastAPI, Depends

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)     #authentication router for user sign-in 
app.include_router(resourceurl.router)  #resourceurl router for all the apps logic operations. 