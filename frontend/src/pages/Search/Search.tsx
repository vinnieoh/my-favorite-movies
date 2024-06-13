import React, { useState } from 'react';
import axios from 'axios';
import url_api from "../../service/BaseUrlApi"

interface Movie {
  imdbID: string;
  Title: string;
  Year: string;
  Poster: string;
}

interface MovieDetails {
  Title: string;
  Year: string;
  Released: string;
  Runtime: string;
  Genre: string;
  Director: string;
  Writer: string;
  Actors: string;
  Plot: string;
  Language: string;
  Country: string;
  Awards: string;
  Poster: string;
  Type: string;
  totalSeasons?: string;
  DVD?: string;
  BoxOffice?: string;
}

function Search() {
  const [query, setQuery] = useState<string>('');
  const [movies, setMovies] = useState<Movie[]>([]);
  const [selectedMovieDetails, setSelectedMovieDetails] = useState<MovieDetails | null>(null);

  const key_api = import.meta.env.VITE_KEYMOVIE;

  const searchMovies = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const apiKey = key_api; // Substitua com a sua chave da OMDb API
    const url = `?s=${query}&apikey=${apiKey}`;

    try {
      const response = await url_api.get(url);
      setMovies(response.data.Search);
      setSelectedMovieDetails(null); // Resetar detalhes do filme
    } catch(err) {
      console.error("Erro ao buscar filmes:", err);
    }
  };

  const fetchMovieDetails = async (imdbID: string) => {
    const apiKey = key_api; // Substitua com a sua chave da OMDb API
    const url = `?i=${imdbID}&apikey=${apiKey}`;

    try {
      const response = await url_api.get(url);
      setSelectedMovieDetails(response.data);
    } catch(err) {
      console.error("Erro ao buscar detalhes do filme:", err);
    }
  };

  const saveMovie = async (movie: MovieDetails) => {
    // Substitua com a URL da sua API e a lógica para salvar o filme
    const saveUrl = 'YOUR_API_URL';
    try {
      await axios.post(saveUrl, movie);
      alert('Filme salvo com sucesso!');
    } catch(err) {
      console.error("Erro ao salvar o filme:", err);
    }
  };

  const displayInfo = (label: string, value: string | undefined) => {
    if (!value || value === "N/A") {
      return null;
    }
    return <p><strong>{label}:</strong> {value}</p>;
  };

  return (
    <div className="w-[85%] mx-auto mt-10">
      <form onSubmit={searchMovies}>
        <div className="relative">
          <input 
            type="search" 
            id="default-search" 
            className="block w-full p-4 pl-10 text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500" 
            placeholder="Search Movies" 
            required 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" className="absolute right-2.5 bottom-2.5 px-4 py-2 text-sm font-medium text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Search
          </button>
        </div>
      </form>
  
      <div className="flex flex-wrap mt-8 gap-8">
        {selectedMovieDetails ? (
          <div className="w-full lg:flex lg:items-start lg:space-x-6">
            <img src={selectedMovieDetails.Poster} alt={selectedMovieDetails.Title} className="lg:w-64 h-auto mb-4 shadow-lg" />
            <div className="lg:w-3/4">
              <h3 className="font-bold text-2xl mb-4">{selectedMovieDetails.Title}</h3>
              {displayInfo("Year", selectedMovieDetails.Year)}
              {displayInfo("Released", selectedMovieDetails.Released)}
              {displayInfo("Runtime", selectedMovieDetails.Runtime)}
              {displayInfo("Genre", selectedMovieDetails.Genre)}
              {displayInfo("Director", selectedMovieDetails.Director)}
              {displayInfo("Writer", selectedMovieDetails.Writer)}
              {displayInfo("Actors", selectedMovieDetails.Actors)}
              {displayInfo("Plot", selectedMovieDetails.Plot)}
              {displayInfo("Language", selectedMovieDetails.Language)}
              {displayInfo("Country", selectedMovieDetails.Country)}
              {displayInfo("Awards", selectedMovieDetails.Awards)}
              {displayInfo("Type", selectedMovieDetails.Type)}
              {selectedMovieDetails.totalSeasons && <p><strong>Total Seasons:</strong> {selectedMovieDetails.totalSeasons}</p>}
              {selectedMovieDetails.DVD && <p><strong>DVD Release:</strong> {selectedMovieDetails.DVD}</p>}
              {selectedMovieDetails.BoxOffice && <p><strong>Box Office:</strong> {selectedMovieDetails.BoxOffice}</p>}
              <button onClick={() => saveMovie(selectedMovieDetails)} className="mt-4 px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded shadow">
                Salvar Filme
              </button>
            </div>
          </div>
        ) : (
          movies.map(movie => (
            <div 
              key={movie.imdbID} 
              className="flex flex-col items-center cursor-pointer bg-white shadow-lg rounded-lg p-5 hover:shadow-xl transition-shadow duration-300"
              onClick={() => fetchMovieDetails(movie.imdbID)}
            >
              <img src={movie.Poster} alt={movie.Title} className="w-48 h-auto object-cover mb-3 rounded-lg" />
              <div>
                <h3 className="font-semibold text-lg text-center">{movie.Title}</h3>
                <p className="text-gray-700 text-center">{movie.Year}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
            }
export default Search;