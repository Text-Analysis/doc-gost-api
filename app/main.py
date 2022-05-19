from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import routes

tags_metadata = [
    {
        "name": "documents",
        "description": "Operations with documents",
    },
    {
        "name": "templates",
        "description": "Operations with templates",
    },
    {
        "name": "other",
        "description": "Other operations"
    }
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
