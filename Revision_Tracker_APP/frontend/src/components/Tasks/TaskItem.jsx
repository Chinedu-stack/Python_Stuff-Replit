import React from 'react';
import useTasksStore from '../../hooks/useTasks';

export function TaskItem({ task, onEdit }) {
  const { toggleTask, deleteTask } = useTasksStore();

  const getPriorityClass = (priority) => {
    return `priority-${priority}`;
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className={`task-item ${task.is_completed ? 'completed' : ''}`}>
      <div className="task-checkbox">
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={() => toggleTask(task.id)}
        />
      </div>

      <div className="task-content" onClick={() => !task.is_completed && onEdit(task)}>
        <div className="task-title">{task.title}</div>
        {task.description && <div className="task-description">{task.description}</div>}
        <div className="task-meta">
          <span className={`priority ${getPriorityClass(task.priority)}`}>
            {task.priority}
          </span>
          <span className="date">📅 {formatDate(task.end_date)}</span>
          {task.due_date && (
            <span className="date">⏰ Due: {formatDate(task.due_date)}</span>
          )}
        </div>
      </div>

      <div className="task-actions">
        {!task.is_completed && (
          <button
            className="btn btn-sm btn-secondary"
            onClick={() => onEdit(task)}
            title="Edit"
          >
            ✏️
          </button>
        )}
        <button
          className="btn btn-sm btn-danger"
          onClick={() => deleteTask(task.id)}
          title="Delete"
        >
          🗑️
        </button>
      </div>
    </div>
  );
}
