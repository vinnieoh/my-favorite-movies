import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../service/BaseUrlApi';

export interface Content {
  id: number;
  title?: string;
  name?: string;
  poster_path: string;
  type: 'movie' | 'tvshow';
}

const Home: React.FC = () => {
  const [contents, setContents] = useState<Content[]>([]);
  const [timeframe, setTimeframe] = useState<'week' | 'day'>('week');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(`/conteudos/trending-all-${timeframe}-br`);
        console.log('Response:', response.data);

        const movies = response.data.results.filter((item: any) => item.media_type === 'movie').map((movie: any) => ({
          ...movie,
          type: 'movie',
        }));

        const tvShows = response.data.results.filter((item: any) => item.media_type === 'tv').map((tvShow: any) => ({
          ...tvShow,
          type: 'tvshow',
        }));

        setContents([...movies, ...tvShows]);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [timeframe]);

  const handleContainerClick = (id: number, type: 'movie' | 'tvshow') => {
    navigate(`/${type}/${id}`);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4 text-center">Melhores Filmes e Séries da {timeframe === 'week' ? 'Semana' : 'Dia'}</h1>

      <div className="flex justify-center mb-8">
        <button
          onClick={() => setTimeframe('week')}
          className={`mr-2 px-4 py-2 rounded ${timeframe === 'week' ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
        >
          Semana
        </button>
        <button
          onClick={() => setTimeframe('day')}
          className={`px-4 py-2 rounded ${timeframe === 'day' ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
        >
          Dia
        </button>
      </div>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Conteúdos</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {contents.map(content => (
            <div
              key={content.id}
              className="bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer transform transition duration-300 hover:scale-105"
              onClick={() => handleContainerClick(content.id, content.type)}
            >
              <img src={`https://image.tmdb.org/t/p/w500/${content.poster_path}`} alt={content.title || content.name} className="w-full h-72 object-cover" />
              <div className="p-4">
                <h3 className="text-lg font-bold">{content.title || content.name}</h3>
                <span className="text-sm text-gray-500">{content.type === 'movie' ? 'Filme' : 'Série'}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {contents.length === 0 && (
        <div className="text-center text-gray-500">Nenhum conteúdo disponível</div>
      )}
    </div>
  );
};

export default Home;
