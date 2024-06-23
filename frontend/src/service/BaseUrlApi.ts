import axios from 'axios';


const url_api = 'http://localhost:8000/api/v1';
//const url_api = 'http://172.20.0.1/api/v1';


const api = axios.create({
  baseURL: url_api,
});

export default api;