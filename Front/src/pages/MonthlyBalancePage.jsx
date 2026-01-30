import React, { useEffect, useState } from "react";
import { Container, Typography, Box, TextField, Button, Divider, Alert } from "@mui/material";
import apiClient from "../api/apiClient";
import BalanceDisplay from "../components/BalanceDisplay";
import CategoryPieChart from "../components/CategoryPieChart";
import BalanceBarChart from "../components/BalanceBarChart";

export default function MonthlyBalancePage() {
  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);

  const [data, setData] = useState({ ingresos: 0, gastos: 0, balance: 0, categorias: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchMonthly = async () => {
    try {
      setLoading(true);
      setError("");

      const balRes = await apiClient.get(`/dashboard/balance/${year}/${month}`);
      const resRes = await apiClient.get(`/dashboard/resumen/${year}/${month}`);

      // Ajustá esto al JSON real:
      const balance = Number(balRes.data?.balance ?? 0);

      const items = resRes.data?.resumen_por_categoria ?? [];

      const gastos_por_categoria = items
        .map((item) => ({
          name: item.nombre ?? `Cat ${item.categoria_id}`,
          value: Number(item.total ?? 0),
        }))
        .filter((x) => x.value > 0);


      const ingresos = Number(balRes.data?.total_ingresos ?? 0);
      const gastos = Number(balRes.data?.total_gastos ?? 0);

      setData({
        ingresos,
        gastos,
        balance,
        categorias: gastos_por_categoria,
      });

    } catch (e) {
      console.error(e);
      setError("No se pudo cargar el balance del mes.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMonthly();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Balance Mensual
      </Typography>

      <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", alignItems: "center" }}>
        <TextField
          label="Año"
          type="number"
          value={year}
          onChange={(e) => setYear(Number(e.target.value))}
          sx={{ width: 140 }}
        />
        <TextField
          label="Mes"
          type="number"
          value={month}
          onChange={(e) => setMonth(Number(e.target.value))}
          sx={{ width: 140 }}
          inputProps={{ min: 1, max: 12 }}
        />
        <Button variant="contained" onClick={fetchMonthly} disabled={loading}>
          {loading ? "Cargando..." : "Ver"}
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      <Divider sx={{ my: 3 }} />

      <BalanceDisplay ingresos={data.ingresos} gastos={data.gastos} balance={data.balance} />

      <Box sx={{ display: "flex", flexDirection: { xs: "column", md: "row" }, gap: 4, mt: 3 }}>
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <CategoryPieChart data={data.categorias} />
        </Box>
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <BalanceBarChart ingresos={data.ingresos} gastos={data.gastos} />
        </Box>
      </Box>
    </Container>
  );
}
