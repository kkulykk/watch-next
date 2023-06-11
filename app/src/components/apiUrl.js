import Cookies from 'js-cookie';

export const checkResponse = (fetchResponse) => {
  if (fetchResponse.status === 204) return {};

  const json = fetchResponse.json();

  if (fetchResponse.ok) return json;
  // if (fetchResponse.status === 401)
  //   setTimeout(() => {
  //     Cookies.remove('accessToken');
  //     location.replace('/login');
  //   }, 0);
  else return json;
};
export function recommendationMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:80';

  return process.env.REACT_APP_RECOMMENDATION_MS;
}
export function userMsUrl() {
  if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:3360';

  return process.env.REACT_APP_USER_MS;
}
export function watchlistMsUrl() {
  // if (process.env.REACT_APP_IS_LOCAL) return 'http://localhost:50001';

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
