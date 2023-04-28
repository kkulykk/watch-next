export const checkResponse = (fetchResponse) => {
  if (fetchResponse.status === 204) return {};

  const json = fetchResponse.json();

  if (fetchResponse.ok) return json;
};
export function apiUrl() {
  return 'http://localhost:50001';
}

export function getStandardHeaders() {
  return {
    'Content-Type': 'application/json'
  };
}
