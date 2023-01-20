from app.routers import (ping, gp)
from fastapi import FastAPI, Request, status
import sklearn
import os 

description = "Project Description"
app = FastAPI(
    title="Hackaton 2023 - Group 6 Project",
    description=description,
    version="0.0.0",
    root_path=os.getenv("ROOT_PATH", ""),
    debug=True,  # To get the python traceback when receiving 500 responses.
)

# GET endpoints
app.include_router(ping.router)
app.include_router(gp.router)

app.router.redirect_slashes = False