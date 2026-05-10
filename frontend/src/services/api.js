import axios from "axios";

const API_BASE = "http://localhost:8000/api";

function getAuthHeaders() {
  const token = localStorage.getItem("glof_sentinel_token");
  return token
    ? {
        Authorization: `Bearer ${token}`
      }
    : {};
}

export async function login(username, password) {
  const { data } = await axios.post(`${API_BASE}/token`, { username, password });
  localStorage.setItem("glof_sentinel_token", data.access_token);
  return data;
}

export async function fetchAlerts() {
  const { data } = await axios.get(`${API_BASE}/alerts`, {
    headers: getAuthHeaders()
  });
  return data;
}

export async function fetchHeatmap() {
  const { data } = await axios.get(`${API_BASE}/heatmap/live`, {
    headers: getAuthHeaders()
  });
  return data;
}

export async function startDemoStream(profile = "balanced") {
  const { data } = await axios.post(
    `${API_BASE}/stream`,
    {
      source_name: "Thorthormi Glacier Lake Demo Basin",
      source_type: "demo",
      frame_limit: 180,
      anomaly_profile: profile,
      geofences: [[0.42, 0.32, 0.5, 0.46]]
    },
    {
      headers: getAuthHeaders()
    }
  );
  return data;
}

export function openAlertsSocket(onMessage) {
  const socket = new WebSocket("ws://localhost:8000/ws/alerts");
  socket.onmessage = (event) => onMessage(JSON.parse(event.data));
  socket.onopen = () => socket.send("dashboard.connected");
  return socket;
}
