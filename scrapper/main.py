import os
import json
from datetime import datetime, timedelta
from scraper import obtener_info_revista
from utils import cargar_json, guardar_json, necesita_actualizacion

def main():
    path_entrada = 'data/json/prueba1.json'
    path_salida = 'data/detalles_revistas.json'

    revistas = cargar_json(path_entrada)
    detalles = cargar_json(path_salida)

    for titulo, info in revistas.items():
        if titulo not in detalles or necesita_actualizacion(detalles[titulo].get("ultima_visita")):
            datos = obtener_info_revista(titulo)
            if datos:
                datos["areas"] = info["areas"]
                datos["catalogos"] = info["catalogos"]
                datos["ultima_visita"] = datetime.today().strftime("%Y-%m-%d")
                detalles[titulo] = datos
        else:
            print(f"'{titulo}' ya está actualizado. Saltando.")

    guardar_json(detalles, path_salida)
    print(f"\n✅ Archivo actualizado: {path_salida}")

if __name__ == '__main__':
    main()
