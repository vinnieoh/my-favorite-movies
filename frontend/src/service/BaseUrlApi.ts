import axios from 'axios';


const url_api = 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: url_api,
});

export default api;