import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API_BASE}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Failed to fetch projects', error);
    }
  };

  const createProject = async () => {
    const name = window.prompt("Enter a name for the new project:", "New Edit");
    if (!name) return;

    try {
      const response = await axios.post(`${API_BASE}/projects`, { name });
      navigate(`/project/${response.data.id}`);
    } catch (error) {
      console.error('Failed to create project', error);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>Projects</h1>
        <button 
          onClick={createProject}
          style={{
            padding: '12px 24px',
            fontSize: '1rem',
            fontWeight: 'bold',
            color: '#fff',
            background: '#ff007f',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 15px rgba(255, 0, 127, 0.4)',
            transition: 'transform 0.2s'
          }}
          onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'} 
          onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
          + New Project
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {projects.map((project) => (
          <div 
            key={project.id} 
            onClick={() => navigate(`/project/${project.id}`)}
            style={{
              background: '#1a1a1a',
              padding: '1.5rem',
              borderRadius: '12px',
              border: '1px solid #333',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.borderColor = '#7f00ff';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.borderColor = '#333';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            <h3 style={{ margin: '0 0 0.5rem 0', color: '#fff' }}>{project.name}</h3>
            <p style={{ margin: 0, color: '#888', fontSize: '0.9rem' }}>ID: {project.id}</p>
          </div>
        ))}
        {projects.length === 0 && (
          <p style={{ color: '#888' }}>No projects found. Create one to start!</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
