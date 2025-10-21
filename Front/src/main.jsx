import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { CssBaseline } from '@mui/material'; // 1. Importa el reseteador de CSS

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <CssBaseline /> {/* <-- 2. Añade este componente aquí */}
    <App />         {/* Tu app va justo después    */}
  </React.StrictMode>
);