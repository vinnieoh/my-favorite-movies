import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Importar o hook useNavigate

// Definindo os tipos diretamente no componente
export interface Movie {
  id: number;
  title: string;
  poster_path: string;
}

export interface TVShow {
  id: number;
  name: string;
  poster_path: string;
}

const Home: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [tvShows, setTvShows] = useState<TVShow[]>([]);
  const [timeframe, setTimeframe] = useState<'week' | 'day'>('week'); // Estado para controlar o período de tempo
  const navigate = useNavigate(); // Instanciar o hook useNavigate

  useEffect(() => {
    const fetchData = async () => {
      try {
        const movieResponse = await axios.get(`http://localhost:8000/api/v1/conteudos/trending-all-${timeframe}-br`);
        setMovies(movieResponse.data.results);

        const tvResponse = await axios.get(`http://localhost:8000/api/v1/conteudos/trending-all-${timeframe}-br`);
        setTvShows(tvResponse.data.results);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [timeframe]); // Refazer a busca de dados quando o timeframe mudar

  const handleContainerClick = (id: number, type: 'movie' | 'tvshow') => {
    navigate(`/${type}/${id}`); // Redirecionar para a página de detalhes
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Melhores Filmes e Séries da {timeframe === 'week' ? 'Semana' : 'Dia'}</h1>
      
      <div className="mb-4">
        <button
          onClick={() => setTimeframe('week')}
          className={`mr-2 px-4 py-2 ${timeframe === 'week' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Semana
        </button>
        <button
          onClick={() => setTimeframe('day')}
          className={`px-4 py-2 ${timeframe === 'day' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
        >
          Dia
        </button>
      </div>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-4">Filmes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {movies.map(movie => (
            <div
              key={movie.id}
              className="bg-white shadow-md rounded-md p-4 cursor-pointer"
              onClick={() => handleContainerClick(movie.id, 'movie')}
            >
              <img src={`https://image.tmdb.org/t/p/w500/${movie.poster_path}`} alt={movie.title} className="rounded-md" />
              <h3 className="text-xl font-bold mt-2">{movie.title}</h3>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Séries</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {tvShows.map(show => (
            <div
              key={show.id}
              className="bg-white shadow-md rounded-md p-4 cursor-pointer"
              onClick={() => handleContainerClick(show.id, 'tvshow')}
            >
              <img src={`https://image.tmdb.org/t/p/w500/${show.poster_path}`} alt={show.name} className="rounded-md" />
              <h3 className="text-xl font-bold mt-2">{show.name}</h3>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;
