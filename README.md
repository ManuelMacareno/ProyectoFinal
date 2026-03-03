# Gestor de Gastos App

Aplicación web para gestionar gastos personales, construida con React (Frontend) y FastAPI (Backend).

---

## Prerrequisitos 🛠️

Asegúrate de tener instalados:
* **Python** (versión 3.8 o superior recomendada).
* **Node.js** (versión 16 o superior recomendada) y **npm**.

---

## Configuración del Backend (FastAPI + PostgreSQL + Alembic) ⚙️

1.  **Abrí una terminal** y navegá a la carpeta del backend:
    ```bash
    cd Back
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
5.  **Creá el archivo `.env`** en la carpeta `Back/` (este archivo NO se commitea):
    ```env
    SECRET_KEY=TU_SECRET_KEY_GENERADA
    DATABASE_URL=postgresql+psycopg2://postgres:TU_PASSWORD@localhost:5432/gastos
    ```
    *Para generar una SECRET_KEY segura:*
    ```bash
    python -c "import secrets; print(secrets.token_urlsafe(48))"
    ```
6.  **Base de datos:** Asegurate de tener PostgreSQL corriendo y que exista una base de datos llamada `gastos`.
    *Si no existe, podés crearla desde `psql`:*
    ```sql
    CREATE DATABASE gastos;
    ```
7.  **Ejecutá las migraciones de Alembic** (esto crea las tablas en PostgreSQL):
    ```bash
    alembic upgrade head
    ```
8.  **Ejecutá el servidor de backend:**
    ```bash
    uvicorn app.main:app --reload
    ```
    *El backend estará corriendo en `http://127.0.0.1:8000`.*
    
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
4. **Creá el archivo `.env`** en la carpeta `Front/` (este archivo NO se commitea):
    ```env
    VITE_API_URL=http://localhost:8000
    ```
5.  **Ejecutá el servidor de desarrollo del frontend:**
    ```bash
    npm run dev
    ```
    *La terminal te dará la URL del frontend, usualmente `http://localhost:5173`.*

---

## Acceder a la Aplicación 🌐

Abrí tu navegador web y andá a la dirección que te dio Vite (ej: `http://localhost:5173`). ¡Ya podés usar la aplicación!
