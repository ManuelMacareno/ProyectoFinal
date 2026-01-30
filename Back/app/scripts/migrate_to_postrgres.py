# scripts/migrate_to_postgres.py
import psycopg2
import sqlite3
from app.core.config import settings

def migrate_sqlite_to_postgres():
    # Conectar a SQLite
    sqlite_conn = sqlite3.connect('./gastos.db')
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cur = sqlite_conn.cursor()
    
    # Conectar a PostgreSQL
    postgres_conn = psycopg2.connect(settings.DATABASE_URL)
    postgres_cur = postgres_conn.cursor()
    
    # Migrar usuarios
    sqlite_cur.execute("SELECT * FROM usuarios")
    for row in sqlite_cur.fetchall():
        postgres_cur.execute("""
            INSERT INTO usuarios (id, email, nombre, hashed_password)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (row['id'], row['email'], row['nombre'], row['hashed_password']))
    
    # Migrar categorías
    sqlite_cur.execute("SELECT * FROM categorias")
    for row in sqlite_cur.fetchall():
        postgres_cur.execute("""
            INSERT INTO categorias (id, nombre, tipo, usuario_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (row['id'], row['nombre'], row['tipo'], row['usuario_id']))
    
    # Migrar transacciones
    sqlite_cur.execute("SELECT * FROM transacciones")
    for row in sqlite_cur.fetchall():
        postgres_cur.execute("""
            INSERT INTO transacciones (id, monto, fecha, descripcion, tipo, categoria_id, usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (row['id'], row['monto'], row['fecha'], row['descripcion'], 
              row['tipo'], row['categoria_id'], row['usuario_id']))
    
    postgres_conn.commit()
    print("Migración completada exitosamente!")
    
    sqlite_conn.close()
    postgres_cur.close()
    postgres_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgres()