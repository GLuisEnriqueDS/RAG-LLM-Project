# models.py
from sentence_transformers import SentenceTransformer

# Cargar el modelo una sola vez
modelo_embed = SentenceTransformer('all-MiniLM-L6-v2')