import pickle
import json
from sentence_transformers import SentenceTransformer

modelo_embed = SentenceTransformer('all-MiniLM-L6-v2')

# Cargar ejemplos
with open("examples.json", "r", encoding="utf-8") as f:
    ejemplos = json.load(f)

# Obtener embeddings
preguntas = [e["pregunta"] for e in ejemplos]
embeddings = modelo_embed.encode(preguntas, convert_to_tensor=True)

# Guardar en archivo .pkl
with open("ejemplos_embeds.pkl", "wb") as f:
    pickle.dump({"ejemplos": ejemplos, "embeddings": embeddings}, f)
