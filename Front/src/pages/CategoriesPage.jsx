import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient';
import { 
  Container, Typography, Box, TextField, Button, 
  List, ListItem, ListItemText, Select, MenuItem, 
  InputLabel, FormControl, Grid, IconButton, Modal,
  Paper // <-- 1. IMPORTAMOS 'PAPER'
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

// --- Estilo para el Modal de Edición ---
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

function CategoriesPage() {
  const [categorias, setCategorias] = useState([]);
  
  // --- Estado para el formulario de CREAR ---
  const [nombre, setNombre] = useState('');
  const [tipo, setTipo] = useState('gasto');

  // --- Estado para el Modal de EDITAR ---
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCategoria, setEditingCategoria] = useState(null);
  const [editNombre, setEditNombre] = useState('');
  const [editTipo, setEditTipo] = useState('gasto');


  // 1. Función para cargar las categorías
  const fetchCategorias = async () => {
    try {
      const response = await apiClient.get('/categorias/');
      setCategorias(response.data);
    } catch (error) {
      console.error("Error al cargar categorías:", error);
    }
  };

  // 2. Cargar categorías al iniciar la página
  useEffect(() => {
    fetchCategorias();
  }, []);

  // 3. Función para CREAR una nueva categoría
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!nombre.trim()) {
      alert("Por favor, ingresa un nombre para la categoría.");
      return;
    }
    try {
      await apiClient.post('/categorias/', { nombre, tipo });
      setNombre(''); // Limpiar formulario
      setTipo('gasto');
      fetchCategorias(); // Recargar la lista
    } catch (error) {
      console.error("Error al crear categoría:", error);
      alert("Error al crear la categoría.");
    }
  };

  // 4. Función para BORRAR una categoría (RF-007)
  const handleDelete = async (id) => {
    if (window.confirm("¿Seguro que querés borrar esta categoría?")) {
      try {
        await apiClient.delete(`/categorias/${id}`);
        fetchCategorias(); // Recargar la lista
      } catch (error) {
        console.error("Error al borrar categoría:", error);
        if (error.response && error.response.status === 400) {
          alert(error.response.data.detail);
        } else {
          alert("Error al borrar la categoría.");
        }
      }
    }
  };

  // --- 5. Funciones para el Modal de EDITAR (RF-006) ---
  const handleOpenEditModal = (categoria) => {
    setEditingCategoria(categoria);
    setEditNombre(categoria.nombre);
    setEditTipo(categoria.tipo);
    setIsModalOpen(true);
  };

  const handleCloseEditModal = () => {
    setIsModalOpen(false);
    setEditingCategoria(null);
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!editNombre.trim()) {
      alert("El nombre no puede estar vacío.");
      return;
    }
    try {
      await apiClient.put(`/categorias/${editingCategoria.id}`, {
        nombre: editNombre,
        tipo: editTipo
      });
      fetchCategorias();
      handleCloseEditModal();
    } catch (error) {
      console.error("Error al actualizar categoría:", error);
      alert("Error al actualizar la categoría.");
    }
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Administrar Categorías
      </Typography>

      {/* Formulario para crear Categoría (Este estilo ya es igual al de Transacciones) */}
      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4, p: 2, border: '1px solid #ddd', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom>Nueva Categoría</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField label="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} fullWidth required />
          </Grid>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel id="tipo-label">Tipo</InputLabel>
              <Select labelId="tipo-label" value={tipo} label="Tipo" onChange={(e) => setTipo(e.target.value)}>
                <MenuItem value="gasto">Gasto</MenuItem>
                <MenuItem value="ingreso">Ingreso</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
          <Button type="submit" variant="contained">
            Crear Categoría
          </Button>
        </Box>
      </Box>
      
      {/* Lista de Categorías existentes */}
      <Typography variant="h6" gutterBottom>Categorías Existentes</Typography>
      
      {/* 2. ENVOLVEMOS LA LISTA EN UN 'PAPER' (igual que en TransactionList.jsx) */}
      <Paper elevation={2} sx={{ mt: 2, width: '100%' }}>
        <List>
          {categorias.length === 0 && (
             <ListItem>
                <ListItemText primary="No hay categorías creadas." />
             </ListItem>
          )}
          {categorias.map(cat => (
            <ListItem 
              key={cat.id} 
              divider
              secondaryAction={
                <Box>
                  <IconButton edge="end" aria-label="edit" sx={{ mr: 1 }} onClick={() => handleOpenEditModal(cat)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(cat.id)}>
                    <DeleteIcon />
                  </IconButton>
                </Box>
              }
            >
              <ListItemText 
                primary={cat.nombre} 
                secondary={cat.tipo === 'gasto' ? 'Gasto' : 'Ingreso'}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
      {/* --- FIN DEL CAMBIO DE ESTILO --- */}


      {/* --- Modal de Edición --- */}
      <Modal open={isModalOpen} onClose={handleCloseEditModal}>
        <Box sx={modalStyle} component="form" onSubmit={handleUpdate}>
          <Typography variant="h6">Editar Categoría</Typography>
          <TextField 
            label="Nombre" 
            value={editNombre} 
            onChange={(e) => setEditNombre(e.target.value)} 
            fullWidth 
            required 
            sx={{ mt: 2 }}
          />
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Tipo</InputLabel>
            <Select value={editTipo} label="Tipo" onChange={(e) => setEditTipo(e.target.value)}>
              <MenuItem value="gasto">Gasto</MenuItem>
              <MenuItem value="ingreso">Ingreso</MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
            <Button onClick={handleCloseEditModal} sx={{ mr: 1 }}>Cancelar</Button>
            <Button type="submit" variant="contained">Guardar Cambios</Button>
          </Box>
        </Box>
      </Modal>

    </Container>
  );
}

export default CategoriesPage;