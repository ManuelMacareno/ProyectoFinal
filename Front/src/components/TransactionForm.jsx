import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import {
  Button,
  TextField,
  Box,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Typography,
  Grid,
  CircularProgress,
  Alert,
} from '@mui/material';

function TransactionForm({ onTransactionCreated }) {
  const [monto, setMonto] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [tipo, setTipo] = useState('gasto');
  const [categoriaId, setCategoriaId] = useState('');
  const [categorias, setCategorias] = useState([]);

  const [loadingCategorias, setLoadingCategorias] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Cargar categorías
  useEffect(() => {
    const fetchCategorias = async () => {
      setLoadingCategorias(true);
      try {
        const response = await apiClient.get('/categorias/');
        setCategorias(response.data);
      } catch (err) {
        console.error("Error al cargar categorías:", err);
        setError('No se pudieron cargar las categorías.');
      } finally {
        setLoadingCategorias(false);
      }
    };
    fetchCategorias();
  }, []);

  // Enviar transacción
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!categoriaId) {
      setError('Selecciona una categoría antes de continuar.');
      return;
    }

    setSubmitting(true);
    try {
      const response = await apiClient.post('/transacciones/', {
        monto: parseFloat(monto),
        descripcion,
        tipo,
        categoria_id: parseInt(categoriaId, 10),
      });

      onTransactionCreated(response.data);
      setMonto('');
      setDescripcion('');
      setCategoriaId('');
      setSuccess('Transacción registrada correctamente ✅');
    } catch (err) {
      console.error("Error al crear transacción:", err);
      setError('No se pudo registrar la transacción.');
    } finally {
      setSubmitting(false);
    }
  };

  const categoriasFiltradas = categorias.filter((c) => c.tipo === tipo);

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        mb: 4,
        p: 3,
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 2,
        backgroundColor: 'background.paper',
        boxShadow: 1,
      }}
    >
      <Typography variant="h6" gutterBottom fontWeight={600}>
        Registrar Transacción
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Monto"
            type="number"
            value={monto}
            onChange={(e) => setMonto(e.target.value)}
            fullWidth
            required
            margin="normal"
            inputProps={{ min: 0, step: '0.01' }}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            label="Descripción"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            fullWidth
            required
            margin="normal"
            inputProps={{ maxLength: 60 }}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth margin="normal">
            <InputLabel id="tipo-label">Tipo</InputLabel>
            <Select
              labelId="tipo-label"
              id="tipo-select"
              value={tipo}
              label="Tipo"
              onChange={(e) => {
                setTipo(e.target.value);
                setCategoriaId('');
              }}
            >
              <MenuItem value="gasto">Gasto</MenuItem>
              <MenuItem value="ingreso">Ingreso</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl
            fullWidth
            margin="normal"
            disabled={loadingCategorias || categoriasFiltradas.length === 0}
          >
            <Select
              value={categoriaId}
              onChange={(e) => setCategoriaId(e.target.value)}
              required
              displayEmpty
            >
              <MenuItem value="" disabled>
                <em>Elegir categoría</em>
              </MenuItem>
              {categoriasFiltradas.map((cat) => (
                <MenuItem key={cat.id} value={cat.id}>
                  {cat.nombre}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit"
          variant="contained"
          disabled={submitting}
          endIcon={submitting && <CircularProgress size={20} color="inherit" />}
        >
          {submitting ? 'Guardando...' : 'Agregar Transacción'}
        </Button>
      </Box>
    </Box>
  );
}

export default TransactionForm;
