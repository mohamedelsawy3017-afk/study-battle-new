// api.js - Centralized API client
const API_BASE = "/api";

// --- Token management ---
const getToken = () => localStorage.getItem("sb_token");
const setToken = (token) => localStorage.setItem("sb_token", token);
const clearToken = () => localStorage.removeItem("sb_token");
const getUser = () => JSON.parse(localStorage.getItem("sb_user") || "null");
const setUser = (user) => localStorage.setItem("sb_user", JSON.stringify(user));
const clearUser = () => localStorage.removeItem("sb_user");

function authHeaders() {
  const token = getToken();
  return token
    ? { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    : { "Content-Type": "application/json" };
}

async function request(method, path, body = null) {
    const opts = { method, headers: authHeaders() };
    if (body) opts.body = JSON.stringify(body);
    
    try {
        const res = await fetch(`${API_BASE}${path}`, opts);
        
        // Only redirect on 401 for specific endpoints (not login/register)
        if (res.status === 401 && !path.includes('/auth/')) {
            clearToken();
            clearUser();
            window.location.href = "/login.html";
            return;
        }
        
        if (res.status === 204) return null;
        
        const data = await res.json();
        
        if (!res.ok) {
            // Return error instead of throwing for auth endpoints
            if (path.includes('/auth/')) {
                return Promise.reject(new Error(data.detail || "Authentication failed"));
            }
            throw new Error(data.detail || "Something went wrong");
        }
        
        return data;
        
    } catch (error) {
        if (path.includes('/auth/')) {
            return Promise.reject(error);
        }
        throw error;
    }
}


const api = {
  // Auth
  register: (body) => request("POST", "/auth/register", body),
  login: (body) => request("POST", "/auth/login", body),

  // Users
  getMe: () => request("GET", "/users/me"),
  getMyStats: () => request("GET", "/users/me/stats"),
  getLeaderboard: () => request("GET", "/users/leaderboard"),
  getUserStats: (username) => request("GET", `/users/${username}/stats`),

  // Tasks
  getTasks: () => request("GET", "/tasks/"),
  createTask: (body) => request("POST", "/tasks/", body),
  updateTask: (id, body) => request("PATCH", `/tasks/${id}`, body),
  completeTask: (id) => request("POST", `/tasks/${id}/complete`),
  deleteTask: (id) => request("DELETE", `/tasks/${id}`),
};

export { api, getToken, setToken, clearToken, getUser, setUser, clearUser };
