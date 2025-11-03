import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useThemeToggle } from '../context/ThemeContext'; // 1. Importa el hook del tema
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material'; // Importa IconButton
import Brightness4Icon from '@mui/icons-material/Brightness4'; // Ícono de Luna (dark)
import Brightness7Icon from '@mui/icons-material/Brightness7'; // Ícono de Sol (light)
import { useTheme } from '@mui/material/styles'; // Hook para saber el tema actual

function NavBar() {
  const { token, logout } = useAuth(); 
  const { toggleTheme } = useThemeToggle(); // 2. Obtené la función de toggle
  const theme = useTheme(); // 3. Obtené el tema actual para saber qué ícono mostrar

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <RouterLink to="/transacciones" style={{ textDecoration: 'none', color: 'inherit' }}>
            Gestor de Gastos
          </RouterLink>
        </Typography>
        
        {/* Box movido al final (antes del 'token ? ...') */}
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

          {/* 4. El Botón de Toggle del Tema */}
          <IconButton sx={{ ml: 1 }} onClick={toggleTheme} color="inherit">
            {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>

          {/* Botón de Logout (solo si está logueado) */}
          {token && (
            <Button color="inherit" onClick={logout}>
              Logout
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;