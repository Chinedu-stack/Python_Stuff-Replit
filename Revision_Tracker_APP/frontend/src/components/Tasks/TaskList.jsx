import React, { useEffect, useState } from 'react';
import { Spinner } from '../Common/Common';
import { TaskItem } from './TaskItem';
import { TaskFilter } from './TaskFilter';
import useTasksStore from '../../hooks/useTasks';

export function TaskList({ onEditTask, filterType = 'all' }) {
  const { tasks, loading, fetchTasks, setFilters } = useTasksStore();
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const filterConfig = {};

    if (filterType === 'active') {
      filterConfig.completed = false;
    } else if (filterType === 'completed') {
      filterConfig.completed = true;
    } else if (filterType.startsWith('priority-')) {
      filterConfig.priority = filterType.split('-')[1];
    }

    if (searchTerm) {
      filterConfig.search = searchTerm;
    }

    setFilters(filterConfig);
    fetchTasks();
  }, [filterType, searchTerm, setFilters, fetchTasks]);

  if (loading) {
    return <Spinner />;
  }

  const filteredTasks = tasks.filter((task) => {
    if (filterType === 'today') {
      const today = new Date().toISOString().split('T')[0];
      return task.start_date <= today && task.end_date >= today;
    }
    return true;
  });

  return (
    <div className="task-list-container">
      <TaskFilter searchTerm={searchTerm} onSearchChange={setSearchTerm} />

      {filteredTasks.length === 0 ? (
        <div className="empty-state">
          <p>No tasks here yet 🎉</p>
          <small>Create a new task to get started</small>
        </div>
      ) : (
        <div className="task-list">
          {filteredTasks.map((task) => (
            <TaskItem key={task.id} task={task} onEdit={onEditTask} />
          ))}
        </div>
      )}
    </div>
  );
}
