import os
import json
from datetime import datetime, timedelta

def cargar_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def necesita_actualizacion(ultima_visita_str):
    if not ultima_visita_str:
        return True
    try:
        ultima = datetime.strptime(ultima_visita_str, "%Y-%m-%d").date()
        return (datetime.today().date() - ultima) > timedelta(days=30)
    except:
        return True
