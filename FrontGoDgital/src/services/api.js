import axios from "axios"

const api = axios.create({
  baseURL: "http://localhost:8080/api",
  timeout: 30000,
  // Configuração HTTPS para ambiente corporativo
  // Evita problemas com certificados SSL auto-assinados
})

// Request interceptor para adicionar token
api.interceptors.request.use((config) => {
  const accessToken = localStorage.getItem("accessToken")
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

// Response interceptor para handle refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refreshToken");
        if (!refreshToken) {
          throw new Error("No refresh token available");
        }

        const refreshResponse = await axios.post(
          "http://localhost:8080/api/auth/refresh",
          { refreshToken }
        );

        const { accessToken, refreshToken: newRefreshToken } = refreshResponse.data;

        if (accessToken && newRefreshToken) {
          localStorage.setItem("accessToken", accessToken);
          localStorage.setItem("refreshToken", newRefreshToken);
          
          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error("Refresh token failed:", refreshError);
        
        // Clear tokens and redirect to login
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user");
        
        // Redirect to login page
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
)

export default api
