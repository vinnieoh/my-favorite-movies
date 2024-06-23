import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../service/BaseUrlApi';

interface RouteParams {
  id: string;
  [key: string]: string | undefined;
}

interface Movie {
  adult: boolean;
  backdrop_path: string | null;
  belongs_to_collection: any | null;
  budget: number;
  genres: { id: number; name: string }[];
  homepage: string;
  id: number;
  imdb_id: string;
  original_language: string;
  original_title: string;
  overview: string;
  popularity: number;
  poster_path: string | null;
  production_companies: { id: number; logo_path: string | null; name: string; origin_country: string }[];
  production_countries: { iso_3166_1: string; name: string }[];
  release_date: string;
  revenue: number;
  runtime: number;
  spoken_languages: { english_name: string; iso_639_1: string; name: string }[];
  status: string;
  tagline: string;
  title: string;
  video: boolean;
  vote_average: number;
  vote_count: number;
}

const MovieDetail: React.FC = () => {
  const [movie, setMovie] = useState<Movie | null>(null);
  const { id } = useParams<RouteParams>();

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await api.get<Movie>(`/conteudos/movie-id/${id}`);
        setMovie(response.data);
      } catch (error) {
        console.error('Error fetching movie:', error);
      }
    };

    fetchMovie();
  }, [id]);

  if (!movie) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="relative w-full h-96 mb-8">
        <img src={`https://image.tmdb.org/t/p/original/${movie.backdrop_path}`} alt={movie.title} className="absolute inset-0 w-full h-full object-cover opacity-75" />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
        <div className="relative container mx-auto p-4 flex flex-col justify-end h-full">
          <h1 className="text-4xl font-bold text-white">{movie.title}</h1>
          {movie.tagline && <span className="text-lg text-gray-300">"{movie.tagline}"</span>}
        </div>
      </div>
      <div className="flex flex-col md:flex-row">
        <div className="md:w-1/3 mb-8 md:mb-0">
          <img src={`https://image.tmdb.org/t/p/w500/${movie.poster_path}`} alt={movie.title} className="rounded-md mb-4 w-full" />
          <div className="bg-white shadow-lg rounded-lg p-4">
            <h2 className="text-2xl font-semibold mb-4">Details</h2>
            <ul className="text-gray-700">
              <li><strong>Release Date:</strong> {movie.release_date}</li>
              <li><strong>Runtime:</strong> {movie.runtime} minutes</li>
              <li><strong>Status:</strong> {movie.status}</li>
              <li><strong>Vote Average:</strong> {movie.vote_average}</li>
              <li><strong>Vote Count:</strong> {movie.vote_count}</li>
              <li><strong>Popularity:</strong> {movie.popularity}</li>
              <li><strong>Original Language:</strong> {movie.original_language}</li>
              <li><strong>Budget:</strong> ${movie.budget.toLocaleString()}</li>
              <li><strong>Revenue:</strong> ${movie.revenue.toLocaleString()}</li>
              <li><strong>Genres:</strong> {movie.genres.map(genre => genre.name).join(', ')}</li>
              <li><strong>Production Companies:</strong> {movie.production_companies.map(company => company.name).join(', ')}</li>
              <li><strong>Production Countries:</strong> {movie.production_countries.map(country => country.name).join(', ')}</li>
            </ul>
          </div>
        </div>
        <div className="md:w-2/3 md:pl-8">
          <div className="bg-white shadow-lg rounded-lg p-4 mb-8">
            <h2 className="text-2xl font-semibold mb-4">Overview</h2>
            <p className="text-gray-700">{movie.overview}</p>
          </div>
          {movie.belongs_to_collection && (
            <div className="bg-white shadow-lg rounded-lg p-4 mb-8">
              <h2 className="text-2xl font-semibold mb-4">Collection</h2>
              <p className="text-gray-700">{movie.belongs_to_collection.name}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;
