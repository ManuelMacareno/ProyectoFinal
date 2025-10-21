import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Container, TextField, Button, Typography, Box, Alert, CircularProgress } from '@mui/material'; // Importamos Alert y CircularProgress
import { useNavigate } from 'react-router-dom';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [nombre, setNombre] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState(''); // <-- 1. Nuevo estado para repetir contraseña

  const { register } = useAuth();
  const navigate = useNavigate();

  // --- 2. Estados para los mensajes y carga ---
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');     // Para mensajes de error
  const [success, setSuccess] = useState(''); // Para el mensaje de éxito

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');   // Reseteamos los mensajes
    setSuccess('');
    setLoading(true); // Empezamos a cargar

    // --- 3. Validación de Contraseña (en el Frontend) ---
    if (password !== password2) {
      setError('Las contraseñas no coinciden.');
      setLoading(false);
      return; // Detenemos la ejecución
    }
    if (password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres.');
      setLoading(false);
      return;
    }
    // --- Fin de la validación ---

    try {
      // 4. Llamamos a la función de registro (que ahora puede fallar)
      await register(email, password, nombre);

      // ¡Éxito!
      setSuccess('¡Usuario creado exitosamente! Serás redirigido al login...');

      // Esperamos 2 segundos para que el usuario lea el mensaje
      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (err) {
      // 5. Atrapamos el error que lanzamos desde AuthContext
      // (ej: "El email ya está registrado.")
      setError(err.message);

    } finally {
      setLoading(false); // Dejamos de cargar
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          Crear Cuenta
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 3 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="nombre"
            label="Nombre de Usuario" 
            name="nombre"
            autoComplete="username" 
            autoFocus
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Correo Electrónico"
            name="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Contraseña (mín. 8 caracteres)"
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          {/* --- 6. Nuevo Campo de Repetir Contraseña --- */}
          <TextField
            margin="normal"
            required
            fullWidth
            name="password2"
            label="Repetir Contraseña"
            type="password"
            id="password2"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
          />

          {/* --- 7. Mensajes de Feedback (Error y Éxito) --- */}
          {error && (
            <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mt: 2, width: '100%' }}>
              {success}
            </Alert>
          )}

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading} // Deshabilitamos el botón mientras carga
          >
            {loading ? <CircularProgress size={24} /> : "Registrarse"}
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default RegisterPage;