# Gestor de Gastos App

Aplicación web para gestionar gastos personales, construida con React (Frontend) y FastAPI (Backend).

---

## Prerrequisitos 🛠️

Asegúrate de tener instalados:
* **Python** (versión 3.8 o superior recomendada).
* **Node.js** (versión 16 o superior recomendada) y **npm**.

---

## Configuración del Backend (FastAPI) ⚙️

1.  **Abrí una terminal** y navegá a la carpeta del backend:
    ```bash
    cd back
    ```
2.  **Creá un entorno virtual:**
    ```bash
    python -m venv venv
    ```
3.  **Activá el entorno virtual:**
    * En Windows: `.\venv\Scripts\activate`
    * En macOS/Linux: `source venv/bin/activate`
    *(Verás `(venv)` al principio de la línea de tu terminal)*
4.  **Instalá las dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Ejecutá el servidor de backend:**
    ```bash
    uvicorn app.main:app --reload
    ```
    *El backend estará corriendo en `http://127.0.0.1:8000`.*

---

## Configuración del Frontend (React/Vite) ⚛️

1.  **Abrí OTRA terminal** (dejá la del backend corriendo).
2.  **Navegá a la carpeta del frontend:**
    ```bash
    cd front
    ```
3.  **Instalá las dependencias de Node.js:**
    ```bash
    npm install
    ```
4.  **Ejecutá el servidor de desarrollo del frontend:**
    ```bash
    npm run dev
    ```
    *La terminal te dará la URL del frontend, usualmente `http://localhost:5173`.*

---

## Acceder a la Aplicación 🌐

Abrí tu navegador web y andá a la dirección que te dio Vite (ej: `http://localhost:5173`). ¡Ya podés usar la aplicación!
