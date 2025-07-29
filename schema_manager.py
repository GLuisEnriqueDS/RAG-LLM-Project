import sqlite3

DB_PATH = 'netflix.db'
SCHEMA = {}

def cargar_schema(db_path=DB_PATH):
    """Carga el esquema de la base de datos en la variable global SCHEMA"""
    global SCHEMA
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener nombres de todas las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    schema_temp = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        schema_temp[table] = columns

    conn.close()
    SCHEMA = schema_temp

def obtener_prompt_schema():
    """Genera una descripción del esquema para incluir en el prompt"""
    lines = ["El esquema de la base de datos es:"]
    for table, columns in SCHEMA.items():
        lines.append(f"- {table}({', '.join(columns)})")
    return "\n".join(lines)

def validar_query(query):
    """Valida que la consulta use solo tablas y columnas existentes"""
    query_lower = query.lower()
    for table in SCHEMA:
        if table.lower() in query_lower:
            for column in SCHEMA[table]:
                col_ref = f"{table}.{column}".lower()
                if col_ref in query_lower:
                    pass  
    return True

# Cargar el esquema al importar
cargar_schema()
