import React, { useEffect } from 'react';
import useTasksStore from '../../hooks/useTasks';

export function TaskStats() {
  const { stats, fetchStats } = useTasksStore();

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  if (!stats) return null;

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-number">{stats.total}</div>
        <div className="stat-label">Total Tasks</div>
      </div>
      <div className="stat-card">
        <div className="stat-number">{stats.pending}</div>
        <div className="stat-label">Pending</div>
      </div>
      <div className="stat-card stat-completed">
        <div className="stat-number">{stats.completed}</div>
        <div className="stat-label">Completed</div>
      </div>
      <div className="stat-card stat-warning">
        <div className="stat-number">{stats.overdue}</div>
        <div className="stat-label">Overdue</div>
      </div>
    </div>
  );
}
