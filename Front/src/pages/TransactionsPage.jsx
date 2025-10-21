import React, { useState, useEffect } from 'react';
import { Container, Typography } from '@mui/material';
import apiClient from '../api/apiClient';
import TransactionForm from '../components/TransactionForm'; 
import TransactionList from '../components/TransactionList'; 
import TransactionEditModal from '../components/TransactionEditModal'; // Importa el Modal

function TransactionsPage() {
  const [transactions, setTransactions] = useState([]);
  
  // --- Estado para manejar el Modal ---
  const [isModalOpen, setIsModalOpen] = useState(false);
  // Estado para saber QUÉ transacción estamos editando
  const [editingTransaction, setEditingTransaction] = useState(null); 
  // ----------------------------------------

  // (RF-005) Función para LEER todas las transacciones
  const fetchTransactions = async () => {
    try {
      const response = await apiClient.get('/transacciones/');
      setTransactions(response.data); // Guardamos la lista en el estado
    } catch (error) {
      console.error("Error al cargar transacciones:", error);
    }
  };

  // Cargar las transacciones cuando la página se abre por primera vez
  useEffect(() => {
    fetchTransactions();
  }, []); // El array vacío significa "ejecutar solo una vez"

  // Esta función recarga la lista cuando se CREA una transacción
  const handleTransactionCreated = () => {
    fetchTransactions();
  };

  // (RF-007) Función para BORRAR
  const handleDelete = async (id) => {
    if (window.confirm("¿Estás seguro de que querés borrar esta transacción?")) {
      try {
        await apiClient.delete(`/transacciones/${id}`);
        // Si el borrado fue exitoso, recargamos la lista
        fetchTransactions();
      } catch (error) {
        console.error("Error al borrar la transacción:", error);
      }
    }
  };

  // --- Funciones para abrir y cerrar el Modal (RF-006) ---
  const handleOpenEditModal = (transaction) => {
    setEditingTransaction(transaction); // Guarda la transacción a editar
    setIsModalOpen(true);               // Abre el modal
  };

  const handleCloseEditModal = () => {
    setEditingTransaction(null); // Limpia la transacción
    setIsModalOpen(false);       // Cierra el modal
  };

  // Se llama cuando el modal avisa que terminó de actualizar
  const handleTransactionUpdated = () => {
    handleCloseEditModal(); // Cierra el modal
    fetchTransactions();    // Recarga la lista de transacciones
  };
  // ------------------------------------------------

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Mis Transacciones
      </Typography>
      
      {/* (RF-004) El formulario para CREAR */}
      <TransactionForm onTransactionCreated={handleTransactionCreated} />

      {/* (RF-005, RF-006, RF-007) La lista para LEER, EDITAR y BORRAR */}
      <TransactionList 
        transactions={transactions} 
        onDelete={handleDelete}
        onEdit={handleOpenEditModal} // Le pasamos la función de editar
      />

      {/* Renderiza el Modal (solo si hay una transacción para editar) */}
      {editingTransaction && (
        <TransactionEditModal
          open={isModalOpen}
          onClose={handleCloseEditModal}
          onUpdated={handleTransactionUpdated}
          transaction={editingTransaction}
        />
      )}
    </Container>
  );
}

export default TransactionsPage;