const runtimeConfig = window.__SIMOPS_CONFIG__ || {};
const API_BASE_URL = runtimeConfig.apiBaseUrl || import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function buildUrl(path, params = {}) {
  const url = new URL(path, API_BASE_URL);

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  });

  return url.toString();
}

async function readJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      Accept: "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

export async function fetchEvents(filters) {
  return readJson(
    buildUrl("/events", {
      severity: filters.severity,
      service_name: filters.serviceName,
      limit: filters.limit,
    }),
  );
}

export async function fetchEventById(eventId) {
  return readJson(buildUrl(`/events/${eventId}`));
}

