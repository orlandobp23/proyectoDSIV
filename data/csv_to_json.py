import csv
import pandas as pd
import json
import os


revistas = {}

folder_areas = "data/csv/areas"
folder_catalogos = "data/csv/catalogos"
ruta_salida = "data/json/revistas.json"

# leer areas
for archivo in os.listdir(folder_areas):
    area = archivo.replace(".csv", "").upper()
    ruta = os.path.join(folder_areas, archivo)
    df = pd.read_csv(ruta, encoding="latin1")
    

for titulo in df['TITULO:']:
    titulo_limpio = titulo.strip().lower()
    if titulo_limpio not in revistas:
        revistas[titulo_limpio] = {"areas":[],"catalogos":[]}
    if area not in revistas[titulo_limpio]["areas"]:
        revistas[titulo_limpio]["areas"].append(area)   


# leer catalogos
for archivo in os.listdir(folder_catalogos):
    catalogo = archivo.replace(".csv","").upper()
    ruta = os.path.join(folder_catalogos, archivo)
    df = pd.read_csv(ruta, encoding="latin1")
    
for titulo in df['TITULO:']:
    titulo_limpio = titulo.strip().lower()
    if titulo_limpio not in revistas:
        revistas[titulo_limpio] = {"areas":[],"catalogos":[]}
    if catalogo not in revistas[titulo_limpio]["catalogos"]:
        revistas[titulo_limpio]["catalogos"].append(area)

#guardar
with open(ruta_salida, "w", encoding="utf-8") as f:
    json.dump(revistas, f, indent=2, ensure_ascii=False)

    
#verificar
with open(ruta_salida, "r", encoding="utf-8") as f:
    revistas_cargadas = json.load(f)
print(f"{len(revistas_cargadas)} revistas cargadas exitosamente")


