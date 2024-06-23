import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../service/BaseUrlApi';
import { useAuth } from '../../context/Auth';

interface FavoriteContent {
  original_id: number;
  original_language: string;
  overview: string;
  popularity: number;
  vote_average: number;
  vote_count: number;
  genre_ids: string;
  backdrop_path: string;
  poster_path: string;
  is_adult: boolean;
  title: string;
  original_title: string;
  release_date: string;
  video: boolean;
  id: string;
  name?: string;
  original_name?: string;
  first_air_date?: string;
  origin_country?: string;
}

const MyMovies: React.FC = () => {
  const [favorites, setFavorites] = useState<FavoriteContent[]>([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFavorites = async () => {
      if (user) {
        try {
          const response = await api.get('/usuario-conteudos/conteudos', {
            headers: {
              Authorization: `Bearer ${user.token}`,
            },
          });
          setFavorites(response.data);
        } catch (error) {
          console.error('Erro ao buscar conteúdos favoritos:', error);
        }
      }
    };

    fetchFavorites();
  }, [user]);

  const handleContentClick = (content: FavoriteContent) => {
    const type = content.name ? 'tvshow' : 'movie';
    navigate(`/${type}/${content.original_id}`);
  };

  if (!favorites.length) {
    return <div className="text-center text-gray-500">Nenhum conteúdo favorito encontrado.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">Meus Filmes e Séries Favoritos</h1>
      <div className="flex flex-wrap mt-8 gap-8">
        {favorites.map(content => (
          <div
            key={content.id}
            className="bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer transform transition duration-300 hover:scale-105 w-60"
            onClick={() => handleContentClick(content)}
          >
            <div className="relative">
              <img
                src={`https://image.tmdb.org/t/p/w500/${content.poster_path}`}
                alt={content.title || content.name}
                className="w-full h-auto object-cover rounded-lg mb-3"
              />
              {content.vote_average !== undefined && (
                <div className="absolute top-2 left-2 bg-yellow-400 text-black text-xs font-bold px-2 py-1 rounded">
                  {content.vote_average.toFixed(1)}
                </div>
              )}
            </div>
            <div className="text-center p-4">
              <h3 className="font-semibold text-lg mb-1">{content.title || content.name}</h3>
              <p className="text-gray-700 text-sm mb-2">{content.release_date || content.first_air_date}</p>
              <p className="text-gray-600 text-xs line-clamp-3">{content.overview}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyMovies;
