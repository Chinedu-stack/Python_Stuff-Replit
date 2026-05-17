import api from './api';

export const tasksService = {
  async fetchTasks(filters = {}) {
    const params = new URLSearchParams();
    if (filters.completed !== undefined) {
      params.append('is_completed', filters.completed);
    }
    if (filters.priority) {
      params.append('priority', filters.priority);
    }
    if (filters.search) {
      params.append('search', filters.search);
    }
    if (filters.ordering) {
      params.append('ordering', filters.ordering);
    }

    const response = await api.get(`/tasks/?${params.toString()}`);
    return response.data;
  },

  async fetchTaskStats() {
    const response = await api.get('/tasks/stats/');
    return response.data;
  },

  async fetchTodayTasks() {
    const response = await api.get('/tasks/today/');
    return response.data;
  },

  async fetchOverdueTasks() {
    const response = await api.get('/tasks/overdue/');
    return response.data;
  },

  async createTask(taskData) {
    const response = await api.post('/tasks/', taskData);
    return response.data;
  },

  async updateTask(id, taskData) {
    const response = await api.patch(`/tasks/${id}/`, taskData);
    return response.data;
  },

  async deleteTask(id) {
    await api.delete(`/tasks/${id}/`);
  },

  async toggleTask(id, isCompleted) {
    const response = await api.patch(`/tasks/${id}/`, { is_completed: !isCompleted });
    return response.data;
  },
};

export default tasksService;
