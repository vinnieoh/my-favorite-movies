import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../service/BaseUrlApi';
import { useAuth } from '../../context/Auth';

interface RouteParams {
  id: string;
  [key: string]: string | undefined;
}

interface TVShow {
  adult: boolean;
  backdrop_path: string | null;
  created_by: any[];
  episode_run_time: number[];
  first_air_date: string;
  genres: { id: number; name: string }[];
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
  production_countries: { iso_3166_1: string; name: string }[];
  seasons: { air_date: string; episode_count: number; id: number; name: string; overview: string; poster_path: string | null; season_number: number; vote_average: number }[];
  spoken_languages: { english_name: string; iso_639_1: string; name: string }[];
  status: string;
  tagline: string;
  type: string;
  vote_average: number;
  vote_count: number;
}

const TVShowDetail: React.FC = () => {
  const [tvShow, setTvShow] = useState<TVShow | null>(null);
  const { id } = useParams<RouteParams>();
  const { user } = useAuth();

  useEffect(() => {
    const fetchTVShow = async () => {
      try {
        const response = await api.get<TVShow>(`/conteudos/tv-show-id/${id}`);
        setTvShow(response.data);
      } catch (error) {
        console.error('Error fetching TV show:', error);
      }
    };

    fetchTVShow();
  }, [id]);

  const handleAddFavorite = async () => {
    if (!tvShow || !user) return;

    const tvShowData = {
      original_id: tvShow.id,
      original_language: tvShow.original_language,
      overview: tvShow.overview,
      popularity: tvShow.popularity,
      vote_average: tvShow.vote_average,
      vote_count: tvShow.vote_count,
      genre_ids: tvShow.genres.map(genre => genre.id).join(','),
      backdrop_path: tvShow.backdrop_path,
      poster_path: tvShow.poster_path,
      is_adult: tvShow.adult,
      name: tvShow.name,
      original_name: tvShow.original_name,
      first_air_date: tvShow.first_air_date,
      origin_country: tvShow.origin_country.join(','),
    };

    try {
      await api.post('/conteudos/registra-tvshow', tvShowData, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
      });
      alert('Série adicionada aos favoritos com sucesso!');
    } catch (error) {
      console.error('Erro ao adicionar série aos favoritos:', error);
      alert('Erro ao adicionar série aos favoritos.');
    }
  };

  if (!tvShow) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <div className="relative w-full h-96 mb-8">
        <img src={`https://image.tmdb.org/t/p/original/${tvShow.backdrop_path}`} alt={tvShow.name} className="absolute inset-0 w-full h-full object-cover opacity-75" />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
        <div className="relative container mx-auto p-4 flex flex-col justify-end h-full">
          <h1 className="text-4xl font-bold text-white">{tvShow.name}</h1>
          <span className="text-lg text-gray-300">{tvShow.tagline}</span>
        </div>
      </div>
      <div className="flex flex-col md:flex-row">
        <div className="md:w-1/3 mb-8 md:mb-0">
          <img src={`https://image.tmdb.org/t/p/w500/${tvShow.poster_path}`} alt={tvShow.name} className="rounded-md mb-4 w-full" />
          <div className="bg-white shadow-lg rounded-lg p-4">
            <h2 className="text-2xl font-semibold mb-4">Details</h2>
            <ul className="text-gray-700">
              <li><strong>First Air Date:</strong> {tvShow.first_air_date}</li>
              <li><strong>Last Air Date:</strong> {tvShow.last_air_date}</li>
              <li><strong>Number of Seasons:</strong> {tvShow.number_of_seasons}</li>
              <li><strong>Number of Episodes:</strong> {tvShow.number_of_episodes}</li>
              <li><strong>Status:</strong> {tvShow.status}</li>
              <li><strong>Vote Average:</strong> {tvShow.vote_average}</li>
              <li><strong>Vote Count:</strong> {tvShow.vote_count}</li>
              <li><strong>Popularity:</strong> {tvShow.popularity}</li>
              <li><strong>Languages:</strong> {tvShow.languages.join(', ')}</li>
              <li><strong>Genres:</strong> {tvShow.genres.map(genre => genre.name).join(', ')}</li>
              <li><strong>Origin Country:</strong> {tvShow.origin_country.join(', ')}</li>
              <li><strong>Production Companies:</strong> {tvShow.production_companies.map(company => company.name).join(', ')}</li>
              <li><strong>Production Countries:</strong> {tvShow.production_countries.map(country => country.name).join(', ')}</li>
              <li><strong>Networks:</strong> {tvShow.networks.map(network => network.name).join(', ')}</li>
            </ul>
            <button
              onClick={handleAddFavorite}
              className="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded"
            >
              Adicionar aos Favoritos
            </button>
          </div>
        </div>
        <div className="md:w-2/3 md:pl-8">
          <div className="bg-white shadow-lg rounded-lg p-4 mb-8">
            <h2 className="text-2xl font-semibold mb-4">Overview</h2>
            <p className="text-gray-700">{tvShow.overview}</p>
          </div>
          <div className="bg-white shadow-lg rounded-lg p-4 mb-8">
            <h2 className="text-2xl font-semibold mb-4">Seasons</h2>
            {tvShow.seasons.map(season => (
              <div key={season.id} className="mb-4">
                <h3 className="text-xl font-semibold">{season.name}</h3>
                <img src={`https://image.tmdb.org/t/p/w500/${season.poster_path}`} alt={season.name} className="rounded-md mb-2 w-full md:w-1/3" />
                <p className="text-gray-700">{season.overview}</p>
                <ul className="text-gray-700">
                  <li><strong>Air Date:</strong> {season.air_date}</li>
                  <li><strong>Episode Count:</strong> {season.episode_count}</li>
                  <li><strong>Vote Average:</strong> {season.vote_average}</li>
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TVShowDetail;
