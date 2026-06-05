# Songs Edit Generator 🎬🎶

An automated video edit generator that bridges the gap between raw footage and a finished music video. Powered by an AI "Director" that analyzes audio beats and applies aesthetic effects.

## 🏗 Project Architecture

This project is divided into distinct, modular parts:

- **`frontend-ui/`**: A modern React application (built with Vite) that provides a dynamic, bold interface for managing projects, uploading music tracks, and adding raw footage.
- **`backend-core/`**: A Python FastAPI server that handles:
  - Project creation and management.
  - Secure media storage into isolated project folders (`storage/projects/<id>/`).
  - Upcoming integration with Whisper (lyrics), Librosa (beats), and FFmpeg (rendering).
- **`automation-n8n/`**: Workflows for the LLM agent that acts as the "Edit Director".
- **`docs/`**: Product specifications and detailed MVP requirements.

## 🚀 Getting Started

To run the full stack locally, you will need two separate terminal windows—one for the backend and one for the frontend.

### Prerequisites
- **Node.js** (v16+ recommended)
- **Python** (3.9+ recommended)
- **FFmpeg** (Required for the upcoming rendering phase. Install via `brew install ffmpeg` on macOS)

### 1. Start the Backend API (FastAPI)

Open a new terminal and navigate to the project root:

```bash
cd backend-core

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
```
The backend API will be running at `http://localhost:8000`.

### 2. Start the Frontend App (React/Vite)

Open a second terminal window and navigate to the project root:

```bash
cd frontend-ui

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
The frontend UI will be running at `http://localhost:5173`. Open this URL in your browser to start creating projects!

## 📂 Storage Structure

All uploaded media is kept locally in the backend. When a new project is created, the system generates an isolated folder structure:
```text
backend-core/storage/projects/<project_id>/
├── raw_audio/    # The main track (.mp3, .wav)
└── raw_video/    # Uploaded footage (.mp4)
```

## 📝 Roadmap
1. **Phase 1**: Ingestion & Storage (Completed)
2. **Phase 2**: Acoustic & Metric Analysis (Whisper & Librosa)
3. **Phase 3**: Mechanical Layout (JSON generation)
4. **Phase 4**: Creative Enrichment (n8n/LLM Agent)
5. **Phase 5**: Final Render (FFmpeg)
