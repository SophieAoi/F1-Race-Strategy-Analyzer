const BASE_URL = "http://localhost:8010";

async function getJson(path) {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${response.status}`);
  }
  return response.json();
}

export function fetchSessions(year) {
  return getJson(`/sessions?year=${year}`);
}

export function fetchDrivers(year, event) {
  return getJson(`/session/${year}/${encodeURIComponent(event)}/drivers`);
}

export function fetchStints(year, event) {
  return getJson(`/session/${year}/${encodeURIComponent(event)}/stints`);
}

export function fetchPace(year, event, drivers, window = 3) {
  return getJson(
    `/session/${year}/${encodeURIComponent(event)}/pace?drivers=${drivers.join(",")}&window=${window}`
  );
}

export function fetchPitStops(year, event) {
  return getJson(`/session/${year}/${encodeURIComponent(event)}/pitstops`);
}
