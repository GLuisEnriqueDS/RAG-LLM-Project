import streamlit as st
import os
import pandas as pd
import sqlite3
import warnings
import google.generativeai as genai
from generar_consulta import generar_sql
from schema_manager import validar_query, obtener_prompt_schema



# Configurar Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
warnings.filterwarnings("ignore")

# Conexión a la base de datos SQLite
conn = sqlite3.connect("netflix.db")
conn.row_factory = sqlite3.Row  # Acceso por nombre de columna

# --- Nueva función añadida ---
def ejecutar_consulta_segura(conn, consulta_sql):
    """Ejecuta una consulta con validación previa"""
    if not validar_query(consulta_sql):
        raise ValueError("La consulta hace referencia a tablas o columnas no existentes")
    
    # Verificar que sea una consulta SELECT
    if not consulta_sql.strip().upper().startswith(('SELECT', 'WITH')):
        raise ValueError("Solo se permiten consultas SELECT o WITH")
    
    return pd.read_sql_query(consulta_sql, conn)

# Streamlit UI
st.set_page_config(page_title="SQL Analyzer Bot", page_icon="📊")
st.title("🎬 Generador y Analizador de Consultas (SQLite Netflix)")

st.markdown("Escribe tu pregunta en lenguaje natural y el bot generará una consulta SQL, la ejecutará y analizará los resultados.")

# Inicializar memoria de historial
if "historial_consultas" not in st.session_state:
    st.session_state.historial_consultas = []

# Input
pregunta = st.text_area("🔍 Escribe tu pregunta")

if st.button("Generar y Analizar"):
    if not pregunta:
        st.warning("Por favor ingresa una pregunta.")
    else:
        with st.spinner("Generando consulta..."):
            try:
                consulta_sql, prompt = generar_sql(pregunta)
                st.success("✅ Consulta generada:")
                st.code(consulta_sql, language="sql")

                # Limpiar SQL
                consulta_sql_limpia = consulta_sql
                if consulta_sql.startswith("```sql"):
                    consulta_sql_limpia = consulta_sql[6:]
                if consulta_sql_limpia.endswith("```"):
                    consulta_sql_limpia = consulta_sql_limpia[:-3]

                consulta_sql_limpia = consulta_sql_limpia.strip().replace('\\n', '\n').replace('\\t', ' ')

                st.text("Consulta limpia para ejecución:")
                st.text(repr(consulta_sql_limpia))

                # --- Modificación del bloque de ejecución ---
                try:
                    # Ejecutar la consulta en SQLite con validación
                    st.info("🔎 Ejecutando en SQLite...")
                    df = ejecutar_consulta_segura(conn, consulta_sql_limpia)

                    # Guardar historial
                    st.session_state.historial_consultas.append({
                        "pregunta": pregunta,
                        "sql": consulta_sql_limpia
                    })

                    # Mostrar resultados
                    st.success("📊 Resultados obtenidos:")
                    st.dataframe(df)

                    if not df.empty:
                        with st.spinner("🤖 Analizando con Gemini..."):
                            try:
                                csv_data = df.head(20).to_csv(index=False)
                                prompt_gemini = f"""
                                Tengo una tabla con resultados de una consulta SQL. Analiza los datos y dame conclusiones claras y breves sobre lo que se observa. 
                                Aquí están los datos en CSV:
                                {csv_data}
                                """
                                model = genai.GenerativeModel("gemini-2.0-flash")
                                response = model.generate_content(prompt_gemini)
                                st.markdown("### 🤖 Análisis por IA")
                                st.write(response.text)
                            except Exception as ai_error:
                                st.error(f"Error en el análisis con IA: {str(ai_error)}")
                    else:
                        st.warning("La consulta no devolvió resultados.")
                        
                except ValueError as ve:
                    st.error(f"Error de validación: {str(ve)}")
                    st.info("Esquema actual de la base de datos:")
                    st.text(obtener_prompt_schema())
                except sqlite3.Error as e:
                    st.error(f"Error de SQL: {str(e)}")
                    st.text("Consulta que falló:")
                    st.text(consulta_sql_limpia)
                    
            except Exception as e:
                st.error(f"Ocurrió un error al generar la consulta: {str(e)}")

# Historial en la barra lateral
with st.sidebar:
    st.markdown("## 🕓 Historial")
    if st.session_state.historial_consultas:
        for i, item in enumerate(reversed(st.session_state.historial_consultas[-10:]), 1):
            st.markdown(f"**{i}.** {item['pregunta']}")
            st.code(item['sql'], language="sql")
    else:
        st.info("Sin consultas previas.")