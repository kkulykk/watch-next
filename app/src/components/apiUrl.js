export const checkResponse = (fetchResponse) => {
  if (fetchResponse.status === 204) return {};

  const json = fetchResponse.json();

  if (fetchResponse.ok) return json;
};

export function movieSearchMsUrl() {
  return process.env.REACT_APP_MOVIE_SEARCH_MS;
}
export function recommendationMsUrl() {
  return process.env.REACT_APP_RECOMMENDATION_MS;
}
export function userMsUrl() {
  return process.env.REACT_APP_USER_MS;
}
export function watchlistMsUrl() {
  return process.env.REACT_APP_WATCHLIST_MS;
}
export function analyticsMsUrl() {
  return process.env.REACT_APP_ANALYTICS_MS;
}

export function getStandardHeaders() {
  return {
    'Content-Type': 'application/json'
  };
}
