import os
import uuid
import shutil
import json
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi import BackgroundTasks

try:
    from faster_whisper import WhisperModel
    # Load model globally to avoid loading it on every request
    whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
except ImportError:
    whisper_model = None

router = APIRouter()

PROJECTS_DIR = "storage/projects"

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: str

class ProjectResponse(BaseModel):
    id: str
    name: str
    language: Optional[str] = None
    duration: Optional[float] = None
    language_probability: Optional[float] = None
    lyrics: Optional[str] = None
    bpm: Optional[float] = None

def get_project_metadata(project_path: str) -> dict:
    metadata_path = os.path.join(project_path, "metadata.json")
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def get_project_name(project_path: str, default_name: str) -> str:
    data = get_project_metadata(project_path)
    return data.get("name", default_name)

def update_project_metadata(project_path: str, data: dict):
    metadata_path = os.path.join(project_path, "metadata.json")
    current_data = get_project_metadata(project_path)
    current_data.update(data)
    with open(metadata_path, "w") as f:
        json.dump(current_data, f)

def set_project_name(project_path: str, name: str):
    update_project_metadata(project_path, {"name": name})

def process_audio_bpm(project_path: str, audio_file_path: str):
    try:
        import librosa
        y, sr = librosa.load(audio_file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)
        update_project_metadata(project_path, {"bpm": round(bpm, 1)})
        print(f"Detected BPM {bpm} for project {project_path}")
    except Exception as e:
        print(f"Error extracting BPM: {e}")

def process_audio_metadata(project_path: str, audio_file_path: str):

    if not whisper_model:
        print("Whisper model not loaded, skipping transcription.")
        return
    try:
        segments, info = whisper_model.transcribe(audio_file_path, beam_size=1)
        # Save initial info quickly so the UI can update
        update_project_metadata(project_path, {
            "language": info.language,
            "duration": info.duration,
            "language_probability": info.language_probability
        })
        print(f"Detected language '{info.language}' for project {project_path}")
        
        # Extract BPM before consuming segments for lyrics
        process_audio_bpm(project_path, audio_file_path)
        
        # Now consume segments to get lyrics (this takes time)
        lyrics = "\n".join([segment.text.strip() for segment in segments])
        update_project_metadata(project_path, {
            "lyrics": lyrics
        })
        print(f"Lyrics extracted for project {project_path}")
    except Exception as e:
        print(f"Error during whisper transcription: {e}")

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
            meta = get_project_metadata(project_path)
            name = meta.get("name", f"Project {pid[:8]}")
            lang = meta.get("language")
            duration = meta.get("duration")
            prob = meta.get("language_probability")
            lyrics = meta.get("lyrics")
            bpm = meta.get("bpm")
            projects.append({"id": pid, "name": name, "language": lang, "duration": duration, "language_probability": prob, "lyrics": lyrics, "bpm": bpm})
    return projects

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    meta = get_project_metadata(project_path)
    name = meta.get("name", f"Project {project_id[:8]}")
    lang = meta.get("language")
    duration = meta.get("duration")
    prob = meta.get("language_probability")
    lyrics = meta.get("lyrics")
    bpm = meta.get("bpm")
    return {"id": project_id, "name": name, "language": lang, "duration": duration, "language_probability": prob, "lyrics": lyrics, "bpm": bpm}

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, data: ProjectUpdate):
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    set_project_name(project_path, data.name)
    return {"id": project_id, "name": data.name}

@router.delete("/projects/{project_id}")
def delete_project(project_id: str):
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        raise HTTPException(status_code=404, detail="Project not found")
    shutil.rmtree(project_path)
    return {"message": "Project deleted successfully"}

@router.post("/projects/{project_id}/audio")
def upload_audio(project_id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    project_audio_dir = os.path.join(project_dir, "raw_audio")
    if not os.path.exists(project_audio_dir):
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_path = os.path.join(project_audio_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    background_tasks.add_task(process_audio_metadata, project_dir, file_path)
    
    return {"message": "Audio uploaded successfully", "filename": file.filename}

@router.post("/projects/{project_id}/transcribe")
def retry_transcription(project_id: str, background_tasks: BackgroundTasks):
    project_dir = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail="Project not found")
        
    audio_dir = os.path.join(project_dir, "raw_audio")
    if not os.path.exists(audio_dir):
        raise HTTPException(status_code=400, detail="No audio to transcribe")
        
    files = [f for f in os.listdir(audio_dir) if os.path.isfile(os.path.join(audio_dir, f))]
    if not files:
        raise HTTPException(status_code=400, detail="No audio to transcribe")
        
    audio_file_path = os.path.join(audio_dir, files[0])
    
    # Clear lyrics so the frontend shows the loading animation again
    update_project_metadata(project_dir, {"lyrics": None})
    
    background_tasks.add_task(process_audio_metadata, project_dir, audio_file_path)
    
    return {"message": "Transcription task restarted"}

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
