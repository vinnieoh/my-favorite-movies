import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../service/BaseUrlApi';
import { useAuth } from '../../context/Auth';

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

interface Comment {
  id: string;
  user_id: string;
  media_id: number;
  media_type: string;
  content: string;
  likes: number;
  username?: string;  // Adicionado para exibição
}

const MovieDetail: React.FC = () => {
  const [movie, setMovie] = useState<Movie | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState<string>('');
  const { id } = useParams<RouteParams>();
  const { user } = useAuth();

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await api.get<Movie>(`/conteudos/movie-id/${id}`);
        setMovie(response.data);
      } catch (error) {
        console.error('Error fetching movie:', error);
      }
    };

    const fetchComments = async () => {
      try {
        const response = await api.get(`/comentario/comentarios/${id}`);
        const commentsData = response.data;

        const userIds = commentsData.map((comment: Comment) => comment.user_id);
        const uniqueUserIds = [...new Set(userIds)];

        const usersResponse = await api.get(`/usuario/`, {
          params: {
            ids: uniqueUserIds.join(','),
          },
        });

        const users = usersResponse.data;
        const commentsWithUsernames = commentsData.map((comment: Comment) => ({
          ...comment,
          username: users.find((user: any) => user.id === comment.user_id)?.username || 'Unknown',
        }));

        setComments(commentsWithUsernames);
      } catch (error) {
        console.error('Error fetching comments:', error);
      }
    };

    fetchMovie();
    fetchComments();
  }, [id]);

  const addToFavorites = async () => {
    if (user && movie) {
      const movieData = {
        original_id: movie.id,
        original_language: movie.original_language,
        overview: movie.overview,
        popularity: movie.popularity,
        vote_average: movie.vote_average,
        vote_count: movie.vote_count,
        genre_ids: movie.genres.map(genre => genre.id).join(', '),
        backdrop_path: movie.backdrop_path,
        poster_path: movie.poster_path,
        is_adult: movie.adult,
        title: movie.title,
        original_title: movie.original_title,
        release_date: movie.release_date,
        video: movie.video
      };

      try {
        await api.post('/conteudos/registra-filme', movieData, {
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        });
        alert('Filme adicionado aos favoritos com sucesso!');
      } catch (error) {
        console.error('Erro ao adicionar filme aos favoritos:', error);
      }
    } else {
      alert('Você precisa estar logado para adicionar filmes aos favoritos.');
    }
  };

  const handleAddComment = async () => {
    if (user && newComment.trim()) {
      const commentData = {
        user_id: user.id,
        media_id: Number(id),
        media_type: 'movie',
        content: newComment,
        likes: 0,
      };

      try {
        await api.post('/comentario/comentarios', commentData, {
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        });
        setNewComment('');
        const response = await api.get(`/comentario/comentarios/${id}`);
        const commentsData = response.data;

        const userIds = commentsData.map((comment: Comment) => comment.user_id);
        const uniqueUserIds = [...new Set(userIds)];

        const usersResponse = await api.get(`/usuario/`, {
          params: {
            ids: uniqueUserIds.join(','),
          },
        });

        const users = usersResponse.data;
        const commentsWithUsernames = commentsData.map((comment: Comment) => ({
          ...comment,
          username: users.find((user: any) => user.id === comment.user_id)?.username || 'Unknown',
        }));

        setComments(commentsWithUsernames);
      } catch (error) {
        console.error('Error adding comment:', error);
      }
    }
  };

  const handleDeleteComment = async (commentId: string) => {
    if (user) {
      try {
        await api.delete(`/comentario/comentarios/${commentId}`, {
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        });
        setComments(comments.filter(comment => comment.id !== commentId));
      } catch (error) {
        console.error('Error deleting comment:', error);
      }
    }
  };

  const handleLikeComment = async (commentId: string) => {
    const comment = comments.find(comment => comment.id === commentId);
    if (user && comment) {
      try {
        const response = await api.put(`/comentario/comentarios/${commentId}`, {
          media_id: comment.media_id,
          media_type: comment.media_type,
          content: comment.content,
          likes: comment.likes + 1,
        }, {
          headers: {
            Authorization: `Bearer ${user.token}`,
          },
        });
  
        if (response.status === 202) {
          setComments(comments.map(c => c.id === commentId ? { ...c, likes: c.likes + 1 } : c));
        }
      } catch (error) {
        console.error('Error liking comment:', error);
      }
    }
  };

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
            <button
              onClick={addToFavorites}
              className="mt-4 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Adicionar aos Favoritos
            </button>
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
          <div className="mt-8">
            <h2 className="text-2xl font-semibold mb-4">Comentários</h2>
            <div className="mb-4">
              <textarea
                className="w-full p-2 border border-gray-300 rounded"
                rows={4}
                placeholder="Deixe seu comentário..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
              ></textarea>
              <button
                onClick={handleAddComment}
                className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
              >
                Adicionar Comentário
              </button>
            </div>
            <div className="space-y-4">
              {comments.map(comment => (
                <div key={comment.id} className="bg-white shadow-lg rounded-lg p-4">
                  <p className="text-gray-700 font-semibold">{comment.username}</p>
                  <p className="text-gray-700">{comment.content}</p>
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-sm text-gray-500">Likes: {comment.likes}</span>
                    <button
                      onClick={() => handleLikeComment(comment.id)}
                      className="text-sm text-blue-500 hover:underline"
                    >
                      Like
                    </button>
                    {user && user.id === comment.user_id && (
                      <button
                        onClick={() => handleDeleteComment(comment.id)}
                        className="text-sm text-red-500 hover:underline"
                      >
                        Deletar
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;
