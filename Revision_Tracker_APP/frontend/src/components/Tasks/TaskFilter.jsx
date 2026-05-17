import React from 'react';

export function TaskFilter({ searchTerm, onSearchChange }) {
  return (
    <div className="task-filter">
      <input
        type="text"
        placeholder="🔍 Search tasks..."
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
        className="search-input"
      />
    </div>
  );
}
