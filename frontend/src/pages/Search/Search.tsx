import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import url_api from "../../service/BaseUrlApi";

interface Content {
  id: number;
  backdrop_path: string | null;
  original_name?: string;
  original_title?: string;
  overview: string;
  poster_path: string | null;
  media_type: string;
  name?: string;
  title?: string;
  original_language: string;
  genre_ids: number[];
  popularity: number;
  first_air_date?: string;
  release_date?: string;
  vote_average?: number;
  vote_count: number;
  origin_country?: string[];
  type: 'movie' | 'tvshow';
}

function Search() {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<Content[]>([]);
  const navigate = useNavigate();

  const searchContent = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const url = `/conteudos/search-conteudo/${query}`;

    try {
      const response = await url_api.get(url);
      const movies = response.data.results.filter((item: any) => item.media_type === 'movie').map((movie: any) => ({
        ...movie,
        type: 'movie',
      }));

      const tvShows = response.data.results.filter((item: any) => item.media_type === 'tv').map((tvShow: any) => ({
        ...tvShow,
        type: 'tvshow',
      }));

      setResults([...movies, ...tvShows]);
    } catch (err) {
      console.error("Erro ao buscar conteúdo:", err);
    }
  };

  const handleContainerClick = (id: number, type: 'movie' | 'tvshow') => {
    navigate(`/${type}/${id}`);
  };

  return (
    <div className="w-[85%] mx-auto mt-10">
      <form onSubmit={searchContent}>
        <div className="relative">
          <input 
            type="search" 
            id="default-search" 
            className="block w-full p-4 pl-10 text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500" 
            placeholder="Search Movies or TV Shows" 
            required 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" className="absolute right-2.5 bottom-2.5 px-4 py-2 text-sm font-medium text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Search
          </button>
        </div>
      </form>

      <div className="flex flex-wrap mt-8 gap-8 justify-center">
        {results.length > 0 ? (
          results.map(result => (
            <div
              key={result.id}
              className="bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer transform transition duration-300 hover:scale-105 w-60"
              onClick={() => handleContainerClick(result.id, result.type)}
            >
              <div className="relative">
                <img src={`https://image.tmdb.org/t/p/w500/${result.poster_path}`} alt={result.title || result.name} className="w-full h-80 object-cover" />
                {result.vote_average !== undefined && (
                  <div className="absolute top-2 left-2 bg-yellow-400 text-black text-xs font-bold px-2 py-1 rounded">
                    {result.vote_average.toFixed(1)}
                  </div>
                )}
              </div>
              <div className="p-4 text-center">
                <h3 className="font-semibold text-lg mb-1">{result.title || result.name}</h3>
                <p className="text-gray-700 text-sm mb-2">{result.release_date || result.first_air_date}</p>
                <p className="text-gray-600 text-xs line-clamp-3">{result.overview}</p>
                <span className="text-sm text-gray-500 block mt-2">{result.type === 'movie' ? 'Filme' : 'Série'}</span>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center w-full">No results found.</p>
        )}
      </div>
    </div>
  );
}

export default Search;
