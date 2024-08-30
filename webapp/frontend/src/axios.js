import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8002', // A URL base do seu backend FastAPI
  headers: {
    'Content-Type': 'application/json',
  },
});

export default instance;