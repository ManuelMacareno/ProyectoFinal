import React from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    Tooltip, ResponsiveContainer
} from 'recharts'; 
import { Typography, Paper, Box } from '@mui/material'; 
import { useTheme } from '@mui/material/styles';

function BalanceBarChart({ ingresos, gastos }) {
    const theme = useTheme();

    const data = [
        {
            name: 'Balance Mensual',
            Ingresos: ingresos,
            Gastos: gastos,
        },
    ];

    return (
        <Paper sx={{ p: 2, height: 400, width: '100%' }}>
            <Typography variant="h6" gutterBottom align="center">
                Ingresos vs. Gastos (Mes Actual)
            </Typography>

            <ResponsiveContainer width="100%" height="85%">
                <BarChart
                    data={data}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5, }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />

                    <Bar dataKey="Ingresos" fill={theme.palette.success.main} />
                    <Bar dataKey="Gastos" fill={theme.palette.error.main} />
                </BarChart>
            </ResponsiveContainer>

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                    <Box sx={{ width: 14, height: 14, bgcolor: theme.palette.success.main, mr: 1 }} />
                    <Typography variant="body2">Ingresos</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: 14, height: 14, bgcolor: theme.palette.error.main, mr: 1 }} />
                    <Typography variant="body2">Gastos</Typography>
                </Box>
            </Box>
        </Paper>
    );
}

export default BalanceBarChart;