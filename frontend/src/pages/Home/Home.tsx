import { useState, useEffect } from 'react';
import axios from 'axios';
import url_movie from "../../service/BaseUrlMovie"

const key_api = import.meta.env.VITE_KEYMOVIE;

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

function Home() {
  const [filmes, setFilmes] = useState<Movie[]>([]);
  const [paginaAtual, setPaginaAtual] = useState(1);
  const filmesPorPagina = 20;

  useEffect(() => {
    const buscarFilmes = async () => {
      const url = `?s=movie&y=2023&apikey=${key_api}&page=${paginaAtual}`;
      try {
        const resposta = await url_movie.get(url);
        if (resposta.data && resposta.data.Search) {
          setFilmes(resposta.data.Search);
        } else {
          setFilmes([]);
        }
      } catch (erro) {
        console.error('Erro ao buscar filmes:', erro);
      }
    };

    buscarFilmes();
  }, [paginaAtual]);

  const fetchAndSaveMovieDetails = async (imdbID: string) => {
    const url = `?i=${imdbID}&apikey=${key_api}`;
    try {
      const resposta = await url_movie.get<MovieDetails>(url);
      saveMovie(resposta.data); // Salvar filme na API
    } catch (erro) {
      console.error('Erro ao buscar detalhes do filme:', erro);
    }
  };

  const saveMovie = async (movie: MovieDetails) => {
    const saveUrl = 'YOUR_API_URL'; // Substitua com a URL da sua API
    try {
      await axios.post(saveUrl, movie);
      alert('Filme salvo com sucesso!');
    } catch(err) {
      console.error("Erro ao salvar o filme:", err);
    }
  };

  const paginar = (numeroDaPagina: number) => setPaginaAtual(numeroDaPagina);

  return (
    <div className="container mx-auto px-8 py-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filmes.map(filme => (
          <div key={filme.imdbID} className="max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <img src={filme.Poster} alt={filme.Title} className="rounded-t-lg w-full h-90 object-cover" />
            <div className="p-5">
              <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{filme.Title}</h5>
              <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">{filme.Year}</p>
              <button onClick={() => fetchAndSaveMovieDetails(filme.imdbID)} className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                Save Movie
              </button>
            </div>
          </div>
        ))}
      </div>
      <div className="flex justify-center mt-8">
        {[...Array(filmesPorPagina).keys()].map(numero => (
          <button key={numero} onClick={() => paginar(numero + 1)} className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 mx-1 rounded">
            {numero + 1}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Home;
