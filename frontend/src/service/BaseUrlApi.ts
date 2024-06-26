import axios from 'axios';


//const url_api = 'http://localhost:8000/api/v1';
//const url_api = 'http://172.20.0.1/api/v1';

const url_api = ' https://735f-159-89-232-114.ngrok-free.app';


const api = axios.create({
  baseURL: url_api,
});

export default api;