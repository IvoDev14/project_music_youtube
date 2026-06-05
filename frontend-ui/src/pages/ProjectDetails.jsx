import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1';
const HOST = 'http://localhost:8000';

const ProjectDetails = () => {
  const { id } = useParams();
  const [project, setProject] = useState({ id, name: 'Loading...' });
  const [media, setMedia] = useState({ audio: [], video: [] });
  const [isUploading, setIsUploading] = useState(false);
  const audioInputRef = useRef(null);
  const videoInputRef = useRef(null);

  useEffect(() => {
    fetchProjectInfo();
    fetchMedia();
  }, [id]);

  const fetchProjectInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE}/projects/${id}`);
      setProject(response.data);
    } catch (error) {
      console.error('Failed to fetch project info', error);
    }
  };

  const editName = async () => {
    const newName = window.prompt("Enter new project name:", project.name);
    if (!newName || newName === project.name) return;

    try {
      await axios.put(`${API_BASE}/projects/${id}`, { name: newName });
      setProject({ ...project, name: newName });
    } catch (error) {
      console.error('Failed to update project name', error);
    }
  };

  const fetchMedia = async () => {
    try {
      const response = await axios.get(`${API_BASE}/projects/${id}/media`);
      setMedia(response.data);
    } catch (error) {
      console.error('Failed to fetch media', error);
    }
  };

  const handleUpload = async (file, type) => {
    if (!file) return;
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      await axios.post(`${API_BASE}/projects/${id}/${type}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      await fetchMedia();
      if (type === 'audio') {
        // Fetch project info to get the detected language, delay slightly for background task
        setTimeout(fetchProjectInfo, 2000);
        setTimeout(fetchProjectInfo, 5000);
      }
    } catch (error) {
      console.error(`Failed to upload ${type}`, error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <Link to="/" style={{ color: '#888', textDecoration: 'none', marginBottom: '1rem', display: 'inline-block' }}>&larr; Back to Dashboard</Link>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '0.5rem 0', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {project.name}
          <button 
            onClick={editName}
            style={{
              fontSize: '1rem', padding: '4px 12px', background: 'transparent', color: '#ff007f', 
              border: '1px solid #ff007f', borderRadius: '4px', cursor: 'pointer'
            }}
          >
            Edit
          </button>
        </h1>
        <p style={{ color: '#a0a0a0', margin: 0 }}>ID: {id}</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        {/* Audio Section */}
        <div style={{ background: '#1a1a1a', padding: '1.5rem', borderRadius: '12px', border: '1px solid #333' }}>
          <h2 style={{ marginTop: 0, color: '#fff', borderBottom: '1px solid #333', paddingBottom: '1rem' }}>Main Track</h2>
          
          {media.audio.length > 0 ? (
            <div>
              {media.audio.map((audioPath, idx) => (
                <div key={idx} style={{ marginBottom: '1rem' }}>
                  <p style={{ color: '#ccc', wordBreak: 'break-all', fontSize: '0.9rem' }}>{audioPath.split('/').pop()}</p>
                  <audio controls style={{ width: '100%' }}>
                    <source src={`${HOST}${audioPath}`} />
                  </audio>
                  {project.language && (
                    <p style={{ marginTop: '0.5rem', color: '#bbb', fontSize: '0.9rem', fontStyle: 'italic' }}>
                      info of the audio: - Language detected: {project.language}
                    </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#888' }}>No audio track uploaded yet.</p>
          )}

          <input 
            type="file" 
            accept="audio/*" 
            style={{ display: 'none' }} 
            ref={audioInputRef}
            onChange={(e) => handleUpload(e.target.files[0], 'audio')}
          />
          <button 
            disabled={isUploading}
            onClick={() => audioInputRef.current.click()}
            style={{
              width: '100%', padding: '12px', marginTop: '1rem', background: '#333', color: '#fff',
              border: '1px dashed #666', borderRadius: '8px', cursor: isUploading ? 'wait' : 'pointer'
            }}
          >
            {isUploading ? 'Uploading...' : 'Upload Audio (.wav, .mp3)'}
          </button>
        </div>

        {/* Video Section */}
        <div style={{ background: '#1a1a1a', padding: '1.5rem', borderRadius: '12px', border: '1px solid #333' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #333', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
            <h2 style={{ margin: 0, color: '#fff' }}>Footage</h2>
            <div>
              <input 
                type="file" 
                accept="video/*" 
                multiple
                style={{ display: 'none' }} 
                ref={videoInputRef}
                onChange={async (e) => {
                  for(let i=0; i<e.target.files.length; i++) {
                    await handleUpload(e.target.files[i], 'video');
                  }
                }}
              />
              <button 
                disabled={isUploading}
                onClick={() => videoInputRef.current.click()}
                style={{
                  padding: '8px 16px', background: '#7f00ff', color: '#fff',
                  border: 'none', borderRadius: '8px', cursor: isUploading ? 'wait' : 'pointer'
                }}
              >
                {isUploading ? 'Uploading...' : 'Add Videos'}
              </button>
            </div>
          </div>

          {media.video.length > 0 ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
              {media.video.map((videoPath, idx) => (
                <div key={idx} style={{ background: '#000', borderRadius: '8px', overflow: 'hidden' }}>
                  <video controls style={{ width: '100%', display: 'block' }}>
                    <source src={`${HOST}${videoPath}`} />
                  </video>
                  <div style={{ padding: '0.5rem' }}>
                    <p style={{ margin: 0, color: '#aaa', fontSize: '0.8rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {videoPath.split('/').pop()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#888' }}>No footage uploaded yet. Add video clips to start.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProjectDetails;
