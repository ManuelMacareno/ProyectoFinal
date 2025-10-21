import React from 'react';
import { 
  List, ListItem, ListItemText, Typography, Paper, 
  IconButton, Box 
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

// Recibe las props 'onDelete' y 'onEdit' desde la página padre
function TransactionList({ transactions, onDelete, onEdit }) {
  
  if (transactions.length === 0) {
    return <Typography>No hay transacciones registradas.</Typography>;
  }

  return (
    <Paper elevation={2} sx={{ mt: 2 }}>
      <List>
        {transactions.map(t => (
          <ListItem 
            key={t.id} 
            divider
            // "secondaryAction" es el contenedor de los botones
            secondaryAction={
              <Box>
                {/* Botón de Editar (RF-006) */}
                <IconButton 
                  edge="end" 
                  aria-label="edit" 
                  sx={{ mr: 1 }}
                  onClick={() => onEdit(t)} // Llama a 'onEdit' con la transacción 't'
                >
                  <EditIcon />
                </IconButton>
                
                {/* Botón de Borrar (RF-007) */}
                <IconButton 
                  edge="end" 
                  aria-label="delete" 
                  onClick={() => onDelete(t.id)}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            }
          >
            <ListItemText
              primary={t.descripcion}
              secondary={
                <React.Fragment>
                  {/* La fecha */}
                  {new Date(t.fecha).toLocaleDateString()}
                  
                  {/* El monto */}
                  <Typography
                    component="span" 
                    sx={{
                      display: 'inline',
                      fontWeight: 'bold',
                      ml: 2, // Margen izquierdo
                      color: t.tipo === 'gasto' ? 'error.main' : 'success.main'
                    }}
                  >
                    {t.tipo === 'gasto' ? '-' : '+'}${t.monto}
                  </Typography>
                </React.Fragment>
              }
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}

export default TransactionList;