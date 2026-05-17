import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="header-content">
        <Link to="/dashboard" className="logo">
          <h1>📝 Todo App</h1>
        </Link>
        <div className="user-menu">
          <span className="user-email">{user?.email}</span>
          <button onClick={handleLogout} className="btn btn-secondary btn-sm">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}

export function Sidebar({ activeFilter, onFilterChange }) {
  return (
    <aside className="sidebar">
      <nav>
        <div className="nav-section">
          <h3>Views</h3>
          <button
            className={`nav-item ${activeFilter === 'all' ? 'active' : ''}`}
            onClick={() => onFilterChange('all')}
          >
            📋 All Tasks
          </button>
          <button
            className={`nav-item ${activeFilter === 'today' ? 'active' : ''}`}
            onClick={() => onFilterChange('today')}
          >
            📅 Today
          </button>
          <button
            className={`nav-item ${activeFilter === 'active' ? 'active' : ''}`}
            onClick={() => onFilterChange('active')}
          >
            ⏳ Active
          </button>
          <button
            className={`nav-item ${activeFilter === 'completed' ? 'active' : ''}`}
            onClick={() => onFilterChange('completed')}
          >
            ✅ Completed
          </button>
        </div>
        <div className="nav-section">
          <h3>Priority</h3>
          <button
            className={`nav-item ${activeFilter === 'priority-high' ? 'active' : ''}`}
            onClick={() => onFilterChange('priority-high')}
          >
            🔴 High
          </button>
          <button
            className={`nav-item ${activeFilter === 'priority-medium' ? 'active' : ''}`}
            onClick={() => onFilterChange('priority-medium')}
          >
            🟡 Medium
          </button>
          <button
            className={`nav-item ${activeFilter === 'priority-low' ? 'active' : ''}`}
            onClick={() => onFilterChange('priority-low')}
          >
            🟢 Low
          </button>
        </div>
      </nav>
    </aside>
  );
}
