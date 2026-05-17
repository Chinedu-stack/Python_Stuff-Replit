import { create } from 'zustand';
import tasksService from '../services/tasks';

const useTasksStore = create((set, get) => ({
  tasks: [],
  stats: null,
  loading: false,
  error: null,
  filters: {
    completed: null,
    priority: null,
    search: '',
    ordering: '-created_at',
  },

  setFilters: (newFilters) =>
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    })),

  fetchTasks: async () => {
    set({ loading: true, error: null });
    try {
      const { tasks } = get();
      const filters = get().filters;
      const data = await tasksService.fetchTasks(filters);
      set({ tasks: data.results || data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchStats: async () => {
    try {
      const stats = await tasksService.fetchTaskStats();
      set({ stats });
    } catch (error) {
      set({ error: error.message });
    }
  },

  createTask: async (taskData) => {
    try {
      const task = await tasksService.createTask(taskData);
      set((state) => ({ tasks: [task, ...state.tasks] }));
      await get().fetchStats();
      return task;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  updateTask: async (id, taskData) => {
    try {
      const task = await tasksService.updateTask(id, taskData);
      set((state) => ({
        tasks: state.tasks.map((t) => (t.id === id ? task : t)),
      }));
      await get().fetchStats();
      return task;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  toggleTask: async (id) => {
    try {
      const task = get().tasks.find((t) => t.id === id);
      const updated = await tasksService.toggleTask(id, task.is_completed);
      set((state) => ({
        tasks: state.tasks.map((t) => (t.id === id ? updated : t)),
      }));
      await get().fetchStats();
      return updated;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  deleteTask: async (id) => {
    try {
      await tasksService.deleteTask(id);
      set((state) => ({
        tasks: state.tasks.filter((t) => t.id !== id),
      }));
      await get().fetchStats();
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },
}));

export default useTasksStore;
