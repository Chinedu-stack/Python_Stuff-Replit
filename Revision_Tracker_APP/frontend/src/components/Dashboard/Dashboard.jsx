import React, { useState } from 'react';
import { Header, Sidebar } from '../Layout/Layout';
import { TaskStats } from './TaskStats';
import { TaskForm } from '../Tasks/TaskForm';
import { TaskList } from '../Tasks/TaskList';

export function Dashboard() {
  const [activeFilter, setActiveFilter] = useState('all');
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleCloseForm = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  return (
    <div className="dashboard-layout">
      <Header />
      <div className="dashboard-content">
        <Sidebar activeFilter={activeFilter} onFilterChange={setActiveFilter} />

        <main className="main-content">
          <div className="dashboard-header">
            <h2>
              {activeFilter === 'all' && '📋 All Tasks'}
              {activeFilter === 'today' && '📅 Today\'s Tasks'}
              {activeFilter === 'active' && '⏳ Active Tasks'}
              {activeFilter === 'completed' && '✅ Completed Tasks'}
              {activeFilter === 'priority-high' && '🔴 High Priority'}
              {activeFilter === 'priority-medium' && '🟡 Medium Priority'}
              {activeFilter === 'priority-low' && '🟢 Low Priority'}
            </h2>
            <button
              className="btn btn-primary"
              onClick={() => {
                setEditingTask(null);
                setShowTaskForm(true);
              }}
            >
              + New Task
            </button>
          </div>

          <TaskStats />

          <section className="tasks-section">
            <TaskList filterType={activeFilter} onEditTask={handleEditTask} />
          </section>
        </main>
      </div>

      <TaskForm
        isOpen={showTaskForm}
        onClose={handleCloseForm}
        taskToEdit={editingTask}
      />
    </div>
  );
}
