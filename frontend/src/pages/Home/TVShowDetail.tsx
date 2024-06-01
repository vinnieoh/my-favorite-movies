// TVShowDetail.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

interface RouteParams {
  id: string;
}

interface TVShow {
  adult: boolean;
  backdrop_path: string | null;
  created_by: any[];
  episode_run_time: number[];
  first_air_date: string;
  genres: any[];
  homepage: string;
  id: number;
  in_production: boolean;
  languages: string[];
  last_air_date: string;
  last_episode_to_air: any;
  name: string;
  next_episode_to_air: any;
  networks: { id: number; logo_path: string | null; name: string; origin_country: string }[];
  number_of_episodes: number;
  number_of_seasons: number;
  origin_country: string[];
  original_language: string;
  original_name: string;
  overview: string;
  popularity: number;
  poster_path: string | null;
  production_companies: { id: number; logo_path: string | null; name: string; origin_country: string }[];
  production_countries: any[];
  seasons: { air_date: string; episode_count: number; id: number; name: string; overview: string; poster_path: string | null; season_number: number; vote_average: number }[];
  spoken_languages: { english_name: string; iso_639_1: string; name: string }[];
  status: string;
  tagline: string;
  type: string;
  vote_average: number;
  vote_count: number;
}

interface RouteParams {
    id: string;
    [key: string]: string | undefined;
}

const TVShowDetail: React.FC = () => {
  const [tvShow, setTvShow] = useState<TVShow | null>(null);
  const { id } = useParams<RouteParams>();

  useEffect(() => {
    const fetchTVShow = async () => {
      try {
        const response = await axios.get<TVShow>(`http://localhost:8000/api/v1/conteudos/tv-show-id/${id}`);
        setTvShow(response.data);
      } catch (error) {
        console.error('Error fetching TV show:', error);
      }
    };

    fetchTVShow();
  }, [id]);

  if (!tvShow) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">{tvShow.name}</h1>
      <img src={`https://image.tmdb.org/t/p/w500/${tvShow.poster_path}`} alt={tvShow.name} className="rounded-md" />
      <p>{tvShow.overview}</p>
    </div>
  );
};

export default TVShowDetail;
