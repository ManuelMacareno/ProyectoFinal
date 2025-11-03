import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Typography, Paper, Box } from '@mui/material';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF1919'];

function CategoryPieChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <Paper sx={{ p: 2, textAlign: 'center', width: '100%', height: 400 }}>
        <Typography>No hay gastos este mes para mostrar en el gráfico.</Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ p: 2, height: 400, width: '100%' }}>
      <Typography variant="h6" gutterBottom align="center">
        Gastos por Categoría (Mes Actual)
      </Typography>
      <ResponsiveContainer width="100%" height="90%">
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            fill="#8884d8"
            label
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  );
}

export default CategoryPieChart;