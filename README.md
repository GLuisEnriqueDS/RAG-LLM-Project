# RAG-LLM-Project
En este proyecto combinamos modelos de lenguaje con recuperación semántica para convertir preguntas en lenguaje natural en consultas SQL. Usamos un enfoque RAG simplificado, donde ejemplos de preguntas y consultas SQL se embeben y recuperan según su similitud con la consulta del usuario.

📂 Estructura del proyecto
setup_netflix_sqlite.py: Script para crear y poblar la base de datos SQLite.

examples.json: Ejemplos de preguntas y consultas SQL para guía.

precalcular_embeddings.py: Calcula y guarda embeddings para los ejemplos.

generar_consulta.py: Lógica para buscar ejemplos similares y generar consultas con Gemini.

schema_manager.py: Maneja el esquema de la base de datos para validar consultas y construir prompts.

main.py: Interfaz web con Streamlit para interactuar con el sistema.

netflix.db: Base de datos SQLite con los datos de ejemplo.
