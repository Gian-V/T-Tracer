from fastapi import FastAPI

from webapp.routers import gps
from webapp.utilities.variables import db, private_key

app = FastAPI()


@app.on_event('startup')
def on_startup():
    db.load()
    private_key.load()


@app.on_event('shutdown')
def on_shutdown():
    db.close()


app.include_router(gps.router)
