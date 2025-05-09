import csv
import pandas as pd
import json
import os


revistas = {}

folder_areas = "data/csv/areas"
folder_catalogos = "data/csv/catalogos"

for archivo in os.listdir(folder_areas):
    area = archivo.replace(".csv", "").upper()
    ruta = os.path.join(folder_areas, archivo)
    df = pd.read_csv(ruta)
    
    
for titulo in df['TITULO']:
    titulo = titulo.strip().lower()
    if titulo not in revistas:
        revistas[titulo] = {"areas":[],"catalogos":[]}
    if area not in revistas[titulo]["areas"]:
        revistas[titulo]["areas"].append(area)
