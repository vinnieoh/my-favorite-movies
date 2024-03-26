import axios from 'axios';

const urlApiMovie = 'teste';

const url_movie = axios.create({
    baseURL: urlApiMovie,
});


export default url_movie;