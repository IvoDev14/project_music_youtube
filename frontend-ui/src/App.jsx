import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ProjectDetails from './pages/ProjectDetails';

const App = () => {
  return (
    <Router>
      <div style={{
        minHeight: '100vh',
        background: '#0a0a0a',
        color: '#ededed',
        fontFamily: "'Inter', sans-serif"
      }}>
        <nav style={{ padding: '1rem 2rem', borderBottom: '1px solid #333' }}>
          <h2 style={{ margin: 0, background: 'linear-gradient(90deg, #ff007f, #7f00ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', display: 'inline-block' }}>
            Director AI
          </h2>
        </nav>
        <main style={{ padding: '2rem' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/project/:id" element={<ProjectDetails />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App;
