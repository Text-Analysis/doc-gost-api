from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import routes

tags_metadata = [
    {
        "name": "specifications",
        "description": "Operations with specifications",
    },
    {
        "name": "templates",
        "description": "Operations with templates",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
