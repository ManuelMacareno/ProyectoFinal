import React, { useState, useEffect, useCallback } from 'react'; // Importa useCallback
// Importa Skeleton, Alert, Button y Divider
import { Container, Typography, CircularProgress, Box, Skeleton, Alert, Button, Divider } from '@mui/material'; 
import apiClient from '../api/apiClient';
import BalanceDisplay from '../components/BalanceDisplay';
import CategoryPieChart from '../components/CategoryPieChart';
import BalanceBarChart from '../components/BalanceBarChart';

function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null); // Nuevo estado para el error

  // Usamos useCallback para evitar que la función se recree en cada render
  const fetchSummary = useCallback(async () => { 
    try {
      setLoading(true);
      setError(null); // Limpiamos errores anteriores
      const response = await apiClient.get('/dashboard/summary');
      setSummary(response.data);
    } catch (err) {
      console.error("Error al cargar el resumen:", err);
      setError("No se pudo cargar el resumen del dashboard. Intenta de nuevo."); // Guardamos el mensaje de error
    } finally {
      setLoading(false);
    }
  }, []); // useCallback necesita un array de dependencias vacío aquí

  // Llamamos a fetchSummary cuando el componente se monta
  useEffect(() => {
    fetchSummary();
  }, [fetchSummary]); // Ahora useEffect depende de fetchSummary

  // --- 1. Estado de Carga Mejorado con Skeletons ---
  if (loading) {
    return (
      <Container sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          <Skeleton width="40%" /> {/* Skeleton para el título */}
        </Typography>
        
        {/* Skeleton para el BalanceDisplay */}
        <Skeleton variant="rectangular" height={118} sx={{ mb: 4 }} /> 
        
        {/* Skeletons para los gráficos (en layout flex) */}
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 4 }}>
          <Skeleton variant="rectangular" height={400} sx={{ flex: 1 }} />
          <Skeleton variant="rectangular" height={400} sx={{ flex: 1 }} />
        </Box>
      </Container>
    );
  }

  // --- 2. Estado de Error Mejorado con Alert y Retry ---
  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard (Mes Actual)
        </Typography>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchSummary}>
            Reintentar
          </Button>
        }>
          {error}
        </Alert>
      </Container>
    );
  }

  // --- 3. Estado "Normal" (cuando hay datos) ---
  // (El estado 'summary' null/vacío ya lo manejan los componentes hijos)
  return (
    <Container sx={{ mt: 4 }}> 
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard (Mes Actual)
      </Typography>
      
      {/* Balance */}
      <BalanceDisplay
        ingresos={summary?.total_ingresos ?? 0} // Usamos '?? 0' por si acaso
        gastos={summary?.total_gastos ?? 0}
        balance={summary?.balance ?? 0}
      />

      {/* Separador visual opcional */}
      <Divider sx={{ my: 4 }} /> 
      
      {/* Contenedor Flex para los gráficos */}
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', md: 'row' }, 
          gap: 4, 
          // Quitamos el margen superior aquí porque ya lo da el Divider
        }}
      >
        {/* Gráfico de Torta */}
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <CategoryPieChart data={summary?.gastos_por_categoria ?? []} />
        </Box>
        
        {/* Gráfico de Barras */}
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <BalanceBarChart 
            ingresos={summary?.total_ingresos ?? 0}
            gastos={summary?.total_gastos ?? 0}
          />
        </Box>
      </Box>
      
    </Container>
  );
}

export default DashboardPage;