import { watchlistMsUrl, checkResponse } from '../../apiUrl';

export const createWatchlist = async (watchlistName) => {
  const url = `${watchlistMsUrl()}/users/2811/watchlists?watchlist_name=${watchlistName}`;

  return fetch(url, {
    method: 'POST'
  }).then(checkResponse);
};

export const getWatchlists = async () => {
  const url = `${watchlistMsUrl()}/users/2811/watchlists`;

  return fetch(url).then(checkResponse);
};

export const deleteWatchlist = async (watchlistId) => {
  const url = `${watchlistMsUrl()}/users/2811/watchlists/${watchlistId}`;

  return fetch(url, { method: 'DELETE' }).then(checkResponse);
};

export const getWatchlistFilms = async (watchlistId) => {
  const url = `${watchlistMsUrl()}/users/2811/watchlists/${watchlistId}/movies`;

  return fetch(url).then(checkResponse);
};

export const putFilmsToWatchlist = async (watchlistId, movieId) => {
  const url = `${watchlistMsUrl()}/users/2811/watchlists/${watchlistId}/movies/${movieId}`;

  return fetch(url, { method: 'PUT' }).then(checkResponse);
};

export const removeFilmFromWatchlist = async (watchlistId, movieId) => {
  const url = `${watchlistMsUrl()}/users/2811/watchlists/${watchlistId}/movies/${movieId}`;

  return fetch(url, { method: 'DELETE' }).then(checkResponse);
};

export const getFilmDetails = async (movieId) => {
  const url = `https://api.themoviedb.org/3/movie/${movieId}?api_key=${process.env.REACT_APP_TMDB_API_KEY}`;

  return fetch(url, { method: 'GET' }).then(checkResponse);
};
