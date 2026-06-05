import os
import uuid
import shutil
import json
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter()

PROJECTS_DIR = "storage/projects"

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: str
    name: str

def get_project_name(project_path: str, default_name: str) -> str:
    metadata_path = os.path.join(project_path, "metadata.json")
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                data = json.load(f)
                return data.get("name", default_name)
        except Exception:
            return default_name
    return default_name

def set_project_name(project_path: str, name: str):
    metadata_path = os.path.join(project_path, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump({"name": name}, f)

@router.post("/projects", response_model=ProjectResponse)
def create_project(data: Optional[ProjectCreate] = None):
    project_id = str(uuid.uuid4())
    project_path = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(os.path.join(project_path, "raw_audio"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "raw_video"), exist_ok=True)
    
    # Use provided name or default to Project + ID
    name = data.name if data and data.name else f"Project {project_id[:8]}"
    set_project_name(project_path, name)
    
    return {"id": project_id, "name": name}

@router.get("/projects", response_model=List[ProjectResponse])
def list_projects():
    if not os.path.exists(PROJECTS_DIR):
        return []
    projects = []
    for pid in os.listdir(PROJECTS_DIR):
        project_path = os.path.join(PROJECTS_DIR, pid)
        if os.path.isdir(project_path):
            name = get_project_name(project_path, f"Project {pid[:8]}")
            projects.append({"id": pid, "name": name})
    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    name = get_project_name(project_path, f"Project {project_id[:8]}")
    return {"id": project_id, "name": name}

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, data: ProjectUpdate):
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    set_project_name(project_path, data.name)
    return {"id": project_id, "name": data.name}

@router.post("/projects/{project_id}/audio")
def upload_audio(project_id: str, file: UploadFile = File(...)):
    project_audio_dir = os.path.join(PROJECTS_DIR, project_id, "raw_audio")
    if not os.path.exists(project_audio_dir):
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_path = os.path.join(project_audio_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Audio uploaded successfully", "filename": file.filename}

@router.post("/projects/{project_id}/video")
def upload_video(project_id: str, file: UploadFile = File(...)):
    project_video_dir = os.path.join(PROJECTS_DIR, project_id, "raw_video")
    if not os.path.exists(project_video_dir):
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_path = os.path.join(project_video_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Video uploaded successfully", "filename": file.filename}

@router.get("/projects/{project_id}/media")
def list_media(project_id: str):
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail="Project not found")
    
    audio_files = []
    audio_dir = os.path.join(project_dir, "raw_audio")
    if os.path.exists(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]
        
    video_files = []
    video_dir = os.path.join(project_dir, "raw_video")
    if os.path.exists(video_dir):
        video_files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
        
    return {
        "audio": [f"/storage/projects/{project_id}/raw_audio/{f}" for f in audio_files],
        "video": [f"/storage/projects/{project_id}/raw_video/{f}" for f in video_files]
    }
