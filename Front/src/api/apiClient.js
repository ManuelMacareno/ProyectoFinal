import axios from 'axios';

// Crea una instancia de Axios con la URL base de tu API
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // La URL de tu backend FastAPI
});

// ¡La parte mágica! (Interceptor)
// Esto se ejecuta ANTES de CADA petición.
// Toma el token del localStorage y lo pone en la cabecera 'Authorization'.
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;