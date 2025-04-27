import React from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Monitor, LogOut } from 'lucide-react';
import './admin.css';

const Admin: React.FC = () => {
  const navigate = useNavigate();

  const navigateToCourseManager = () => {
    window.location.href = 'https://hexcent.in/course.html';
  };
  

  const navigateToWebScrapingOverview = () => {
    navigate('/Overview');
  };

  const handleLogout = () => {
    // You can clear tokens/session here if needed
    localStorage.removeItem('adminToken'); // if using localStorage
    navigate('/AdminLogin');
  };

  // Generate grid tiles
  const tiles = Array.from({ length: 600 }, (_, i) => (
    <div key={i} className="grid-tile"></div>
  ));

  return (
    <div className="admin-wrapper">
      <div className="grid-background">{tiles}</div>

      <div className="admin-dashboard">
        <h1>Admin Dashboard</h1>

        {/* Logout Button */}
        <button className="logout-button" onClick={handleLogout}>
          <LogOut className="icon" />
          Logout
        </button>

        <div className="dashboard-container">
          <div className="card" onClick={navigateToCourseManager}>
            <h2><BookOpen className="icon" /> Course Manager</h2>
            <p>Manage available courses, add new ones, or update existing courses.</p>
          </div>
          <div className="card" onClick={navigateToWebScrapingOverview}>
            <h2><Monitor className="icon" /> Web Scraping Overview</h2>
            <p>Monitor and manage the status of ongoing web scraping tasks.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Admin;
