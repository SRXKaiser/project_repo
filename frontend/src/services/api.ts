import axios from 'axios';

const api = axios.create({
  baseURL: '',   //falta pal backend
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;