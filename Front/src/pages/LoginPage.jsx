import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
// Importa Alert, Link y Grid
import { Container, TextField, Button, Typography, Box, Alert, Link, Grid } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom'; // Importa RouterLink

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // Estado para mostrar errores
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); 
    try {
      await login(username, password);
    } catch (err) {
      setError(err.message);
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
          Iniciar Sesión
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>

          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Email o Usuario"
            name="username"
            autoComplete="email"
            autoFocus
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Contraseña"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {/* Mostramos el error si existe */}
          {error && (
            <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
              {error}
            </Alert>
          )}

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Ingresar
          </Button>

          {/* --- ENLACE A REGISTRO AGREGADO --- */}
          <Grid container justifyContent="center">
            <Grid item>
              <Typography variant="body2">
                No estás registrado?{' '}
                <Link component={RouterLink} to="/register" variant="body2">
                  Registrate aquí
                </Link>
              </Typography>
            </Grid>
          </Grid>
          {/* --- FIN DEL ENLACE --- */}

        </Box>
      </Box>
    </Container>
  );
}

export default LoginPage;