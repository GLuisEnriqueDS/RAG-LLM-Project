import os
import json
import pickle
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import util
from schema_manager import obtener_prompt_schema
from models import modelo_embed  

# Cargar la API Key de Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def cargar_ejemplos(ruta="examples.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_similares(pregunta_usuario, ruta="ejemplos_embeds.pkl", top_n=3):
    with open(ruta, "rb") as f:
        data = pickle.load(f)
    ejemplos = data["ejemplos"]
    embeddings_ejemplos = data["embeddings"]

    embedding_usuario = modelo_embed.encode(pregunta_usuario, convert_to_tensor=True)
    similitudes = util.cos_sim(embedding_usuario, embeddings_ejemplos)[0]
    top_indices = similitudes.topk(k=top_n).indices.tolist()

    return [ejemplos[i] for i in top_indices]

def generar_prompt(ejemplos_similares, pregunta_usuario):
    prompt = f"""Eres un asistente experto en bases de datos SQLite. 
Tu tarea es generar consultas SQL para la base de datos netflix.db.

{obtener_prompt_schema()}

Reglas importantes:
1. Usa SOLO las tablas y columnas mencionadas arriba
2. Los nombres deben coincidir EXACTAMENTE (incluyendo mayúsculas)
3. Responde únicamente con la consulta SQL, sin explicaciones\n\n"""

    for ej in ejemplos_similares:
        prompt += f"Pregunta: {ej['pregunta']}\nSQL: {ej['sql']}\n\n"
    
    prompt += f"Pregunta: {pregunta_usuario}\nSQL:"
    return prompt

def generar_sql(pregunta_usuario):
    similares = buscar_similares(pregunta_usuario)
    prompt = generar_prompt(similares, pregunta_usuario)
    modelo = genai.GenerativeModel("gemini-2.0-flash")
    respuesta = modelo.generate_content(prompt)
    return respuesta.text.strip(), prompt
