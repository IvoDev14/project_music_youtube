import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import router as v1_router

app = FastAPI(title="Songs Edit Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure base storage directories exist
os.makedirs("storage/projects", exist_ok=True)

# Mount the storage directory so frontend can access media files directly via URL
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Songs Edit Generator API"}
