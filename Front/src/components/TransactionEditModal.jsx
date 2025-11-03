import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import { 
  Button, TextField, Box, Select, MenuItem, InputLabel, 
  FormControl, Typography, Grid, Modal 
} from '@mui/material';

// Estilo para el Modal (para centrarlo)
const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

// Recibimos la transacción a editar (transaction)
// y las funciones para cerrar (onClose) y avisar que se actualizó (onUpdated)
function TransactionEditModal({ open, onClose, transaction, onUpdated }) {
  // Estado interno del formulario
  const [monto, setMonto] = useState(0);
  const [descripcion, setDescripcion] = useState('');
  const [tipo, setTipo] = useState('gasto');
  const [categoriaId, setCategoriaId] = useState('');
  
  const [categorias, setCategorias] = useState([]);

  // 1. Cargar las categorías (igual que en el formulario de crear)
  useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const response = await apiClient.get('/categorias/');
        setCategorias(response.data);
      } catch (error) { console.error("Error al cargar categorías:", error); }
    };
    fetchCategorias();
  }, []);

  // Cuando la 'transaction' que recibimos cambia, llenamos el formulario.
  useEffect(() => {
    if (transaction) {
      setMonto(transaction.monto);
      setDescripcion(transaction.descripcion);
      setTipo(transaction.tipo);
      setCategoriaId(transaction.categoria_id);
    }
  }, [transaction]); // Este efecto se ejecuta cada vez que 'transaction' cambia

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!categoriaId) {
        alert("Por favor, selecciona una categoría.");
        return;
    }
    try {
      // 3. (RF-006) Llamamos al endpoint 'PUT' para ACTUALIZAR
      await apiClient.put(`/transacciones/${transaction.id}`, {
        monto: parseFloat(monto),
        descripcion,
        tipo,
        categoria_id: parseInt(categoriaId)
      });
      
      onUpdated(); // 4. Avisamos a la página que se actualizó (para que recargue la lista)

    } catch (error) {
      console.error("Error al actualizar transacción:", error);
      alert("Error al actualizar la transacción.");
    }
  };

  const categoriasFiltradas = categorias.filter(c => c.tipo === tipo);

  return (
    <Modal
      open={open}
      onClose={onClose}
      aria-labelledby="modal-title"
    >
      <Box sx={modalStyle} component="form" onSubmit={handleSubmit}>
        <Typography id="modal-title" variant="h6" component="h2">
          Editar Transacción
        </Typography>
        
        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} sm={6}>
            <TextField label="Monto" type="number" value={monto} onChange={(e) => setMonto(e.target.value)} fullWidth required />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField label="Descripción" type="text" value={descripcion} onChange={(e) => setDescripcion(e.target.value)} fullWidth required />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Tipo</InputLabel>
              <Select value={tipo} label="Tipo" onChange={(e) => setTipo(e.target.value)}>
                <MenuItem value="gasto">Gasto</MenuItem>
                <MenuItem value="ingreso">Ingreso</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth disabled={categoriasFiltradas.length === 0}>
              <Select value={categoriaId} onChange={(e) => setCategoriaId(e.target.value)} required displayEmpty>
                <MenuItem value="" disabled><em>Elegir categoría</em></MenuItem>
                {categoriasFiltradas.map(cat => (
                  <MenuItem key={cat.id} value={cat.id}>{cat.nombre}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
          <Button onClick={onClose} sx={{ mr: 1 }}>Cancelar</Button>
          <Button type="submit" variant="contained">Guardar Cambios</Button>
        </Box>
      </Box>
    </Modal>
  );
}

export default TransactionEditModal;