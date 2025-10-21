import React, { createContext, useState, useContext, useEffect } from 'react';
import apiClient from '../api/apiClient';
import { useNavigate } from 'react-router-dom';

// 1. Crear el Contexto
const AuthContext = createContext();

// 2. Crear el Proveedor (Provider)
export const AuthProvider = ({ children }) => {
  // Inicializamos el token desde localStorage para mantener la sesión
  const [token, setToken] = useState(localStorage.getItem('access_token') || null);
  const [user, setUser] = useState(null); // (Opcional, si querés guardar datos del user)
  const navigate = useNavigate(); // Hook para redirigir

  // Efecto para actualizar el 'Authorization' header en apiClient si el token cambia
  useEffect(() => {
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('access_token', token);
    } else {
      delete apiClient.defaults.headers.common['Authorization'];
      localStorage.removeItem('access_token');
    }
  }, [token]);

  const login = async (usernameOrEmail, password) => { 
    try {
      const formData = new URLSearchParams();
      // 'username' es el nombre que FastAPI espera del formulario OAuth2
      formData.append('username', usernameOrEmail); 
      formData.append('password', password);

      const response = await apiClient.post('/token', formData);
      
      const { access_token } = response.data;
      setToken(access_token);
      
      navigate('/transacciones');
    } catch (error) {
      console.error('Error en el login:', error);
      throw new Error('Email/Usuario o contraseña incorrectos.');
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    navigate('/login'); // Redirige al login
  };

  const register = async (email, password, nombre) => {
     try {
        // Intentamos crear el usuario
        await apiClient.post('/usuarios/', { email, password, nombre });
        
     } catch (error) {
        console.error('Error en el registro:', error);
        
        // Reenviamos el error específico del backend
        if (error.response && error.response.status === 400) {
          // Este es el error "400 Bad Request" (Email ya registrado)
          throw new Error('El email ya está registrado.');
        } else {
          // Para cualquier otro error (ej: se cayó el servidor)
          throw new Error('Error al registrar el usuario. Intenta de nuevo.');
        }
     }
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

// 3. Hook personalizado para usar el contexto
export const useAuth = () => {
  return useContext(AuthContext);
};