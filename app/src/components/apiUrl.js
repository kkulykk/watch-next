export const checkResponse = (fetchResponse) => {
  if (fetchResponse.status === 204) return {};

  const json = fetchResponse.json();

  if (fetchResponse.ok) return json;
};

export function movieSearchMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:50172';

  return process.env.REACT_APP_MOVIE_SEARCH_MS;
}
export function recommendationMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:50173';

  return process.env.REACT_APP_RECOMMENDATION_MS;
}
export function userMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:50174';

  return process.env.REACT_APP_USER_MS;
}
export function watchlistMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:50175';

  return process.env.REACT_APP_WATCHLIST_MS;
}
export function analyticsMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:50176';

  return process.env.REACT_APP_ANALYTICS_MS;
}

export function getStandardHeaders() {
  return {
    'Content-Type': 'application/json'
  };
}
