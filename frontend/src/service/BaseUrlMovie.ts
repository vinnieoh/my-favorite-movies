import axios from 'axios';

const urlApiMovie = 'https://www.omdbapi.com/';

const url_movie = axios.create({
    baseURL: urlApiMovie,
});


export default url_movie;