import api from './api';

export const authService = {
  async register(email, password, password2, firstName = '', lastName = '') {
    const response = await api.post('/auth/users/register/', {
      email,
      password,
      password2,
      first_name: firstName,
      last_name: lastName,
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data.user;
  },

  async login(email, password) {
    const response = await api.post('/auth/login/', { email, password });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    return response.data;
  },

  async getMe() {
    const response = await api.get('/auth/users/me/');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  },

  getToken() {
    return localStorage.getItem('access_token');
  },
};

export default authService;
