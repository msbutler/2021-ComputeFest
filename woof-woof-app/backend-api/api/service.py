from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from api.routers import data
import api.utils as api_utils

prefix = "/v1"

# api boiler plate code
"""
boiler plate url code

An API (Application Programming Interface) is a set of functions that allows applications to access data
and interact with external software components, operating systems, or microservices.
 To simplify, an API delivers a user response to a system and sends the system's response back to a user.
"""
# Setup FastAPI app
app = FastAPI(
    title="API Service",
    description="API Service",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception hooks

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc)
        }
    )

# Application start/stop hooks

@app.on_event("startup")
async def startup():
    api_utils.ensure_data_loaded()
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

# Routes
@app.get(
    "/",
    summary="Index",
    description="Root api"
)
async def get_index():
    return {
        "message": "Welcome to the API Service"
    }

# Additional routers here
app.include_router(data.router, prefix=prefix)
