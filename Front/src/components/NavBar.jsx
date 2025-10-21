import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';

function NavBar() {
  const { token, logout } = useAuth();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <RouterLink to="/transacciones" style={{ textDecoration: 'none', color: 'inherit' }}>
            Gestor de Gastos
          </RouterLink>
        </Typography>

        <Box>
          {token ? (
            // Si el usuario está logueado
            <>
              <Button color="inherit" component={RouterLink} to="/transacciones">
                Transacciones
              </Button>

              <Button color="inherit" component={RouterLink} to="/dashboard">
                Dashboard
              </Button>

              <Button color="inherit" component={RouterLink} to="/categorias">
                Categorías
              </Button>

              <Button color="inherit" onClick={logout}>
                Logout
              </Button>
            </>
          ) : (
            // Si no está logueado
            <>
              <Button color="inherit" component={RouterLink} to="/login">
                Login
              </Button>
              <Button color="inherit" component={RouterLink} to="/register">
                Registrarse
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;