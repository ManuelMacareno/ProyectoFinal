import React from 'react';
import { Paper, Typography, Box, Grid } from '@mui/material';
import { useTheme } from '@mui/material/styles'; // Import useTheme to access colors

function BalanceDisplay({ ingresos, gastos, balance }) {
  const theme = useTheme(); // Hook to get theme colors

  // Adjusted formatting function (removes explicit sign handling here)
  const formatCurrency = (num) => {
    if (typeof num !== 'number') return '$0.00';
    // Use Math.abs() to format the absolute value, we'll add the sign later
    return `$${Math.abs(num).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  }

  // Determine color and sign based on the balance value
  const balanceColor = balance >= 0 ? theme.palette.success.main : theme.palette.error.main;
  const balanceSign = balance > 0 ? '+' : balance < 0 ? '-' : ''; // Add '+' for positive, keep '-' for negative

  return (
    <Paper sx={{ p: 3, mb: 4 }}>
      <Grid container spacing={2} justifyContent="space-around" textAlign="center">
        
        {/* Ingresos */}
        <Grid item xs={12} md={4}>
          <Typography variant="h6" color={theme.palette.success.main}>Ingresos</Typography>
          <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
            {formatCurrency(ingresos)}
          </Typography>
        </Grid>
        
        {/* Gastos */}
        <Grid item xs={12} md={4}>
          <Typography variant="h6" color={theme.palette.error.main}>Gastos</Typography>
          <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
            {formatCurrency(gastos)}
          </Typography>
        </Grid>
        
        {/* Balance (with conditional color and sign) */}
        <Grid item xs={12} md={4}>
          <Typography variant="h6" color="primary.main">Balance</Typography>
          <Typography 
            variant="h4" 
            sx={{ fontWeight: 'bold' }}
            color={balanceColor} // Use the determined color
          >
            {balanceSign}{formatCurrency(balance)} {/* Prepend the sign */}
          </Typography>
        </Grid>

      </Grid>
    </Paper>
  );
}

export default BalanceDisplay;