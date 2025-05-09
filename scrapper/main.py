import os
import json
from datetime import datetime, timedelta
from scraper import obtener_info_revista
from utils import cargar_json, guardar_json, necesita_actualizacion

def main():
    path_entrada = 'data/json/revistas.json'
    path_salida = 'data/json/detalles_revistas.json'

    revistas = cargar_json(path_entrada)
    detalles = cargar_json(path_salida)

    contador = 0

    for titulo, info in revistas.items():
        if titulo not in detalles or necesita_actualizacion(detalles[titulo].get("ultima_visita")):
            datos = obtener_info_revista(titulo)
            if datos:
                datos["areas"] = info["areas"]
                datos["catalogos"] = info["catalogos"]
                datos["ultima_visita"] = datetime.today().strftime("%Y-%m-%d")
                detalles[titulo] = datos
                contador += 1

                # Guardado cada 10,000 revistas 
                if contador % 10000 == 0:
                    guardar_json(detalles, path_salida)
                    print(f" Progreso guardado: {contador} revistas procesadas")

        else:
            print(f"'{titulo}' ya está actualizado. Saltando.")

    # Guardado final
    guardar_json(detalles, path_salida)
    print(f"\n Archivo final actualizado: {path_salida}")

if __name__ == '__main__':
    main()