// MovieDetail.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

interface RouteParams {
  id: string;
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
  origin_country: string[];
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

interface RouteParams {
    id: string;
    [key: string]: string | undefined;
}

const MovieDetail: React.FC = () => {
  const [movie, setMovie] = useState<Movie | null>(null);
  const { id } = useParams<RouteParams>();

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await axios.get<Movie>(`http://localhost:8000/api/v1/conteudos/movie-id/${id}`);
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
      <h1 className="text-3xl font-bold mb-4">{movie.title}</h1>
      <img src={`https://image.tmdb.org/t/p/w500/${movie.poster_path}`} alt={movie.title} className="rounded-md" />
      <p>{movie.overview}</p>
    </div>
  );
};

export default MovieDetail;
