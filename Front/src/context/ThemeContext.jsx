import React, { createContext, useState, useMemo, useContext } from 'react';
import { createTheme, ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

// Creamos el contexto
const ThemeContext = createContext({
  toggleTheme: () => {}, // Una función vacía por defecto
});

// Hook para usar el contexto
export const useThemeToggle = () => useContext(ThemeContext);

// El Proveedor (Provider) que envolverá tu app
export const ThemeProvider = ({ children }) => {
  // Estado para guardar el modo actual ('light' o 'dark')
  const [mode, setMode] = useState('light');

  // Función para cambiar el modo
  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  // creamos el tema de MUI.
  // useMemo evita que se recalcule en cada render
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode, // Aquí está la magia: 'light' o 'dark'
        },
      }),
    [mode] // Solo se recalcula si 'mode' cambia
  );

  return (
    <ThemeContext.Provider value={{ toggleTheme }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline /> {/* Normaliza los estilos y aplica el fondo (blanco o negro) */}
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};