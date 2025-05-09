import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

BASE_SEARCH_URL = "https://www.scimagojr.com/journalsearch.php?q="

def buscar_url_revista(nombre_revista):
    query = quote(nombre_revista)
    url_busqueda = BASE_SEARCH_URL + query
    print(f"Buscando URL de: {nombre_revista}")
    
    try:
        headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        time.sleep(5)
    except Exception as e:
        print(f"Error en la conexión para {nombre_revista}: {e}")
        return None

    if response.status_code != 200:
        print(f"Error {response.status_code} al buscar '{nombre_revista}'")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    resultado = soup.select_one('a[href*="journalsearch.php?q="][href*="tip=sid"]')

    if resultado:
        perfil_url = "https://www.scimagojr.com/" + resultado.get("href")
        print(f"URL encontrada: {perfil_url}")
        return perfil_url
    else:
        print(f"No se encontró perfil para: {nombre_revista}")
        return None

def scrap_datos_revista(url):
    print(f"Accediendo a perfil: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(5)
    except Exception as e:
        print(f"Error accediendo a {url}: {e}")
        return None

    if response.status_code != 200:
        print(f"Error {response.status_code} al acceder al perfil de la revista")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    def buscar_con_h2(titulo):
        h2 = soup.find('h2', string=lambda t: t and titulo.lower() in t.lower())
        if h2:
            p = h2.find_next_sibling('p')
            if p:
                return p.text.strip()
        return None

    def extraer_h_index():
        h2 = soup.find('h2', string=lambda t: t and "h-index" in t.lower())
        if h2:
            p = h2.find_next_sibling('p')
            if p and 'hindexnumber' in p.get("class", []):
                return p.text.strip()
        return None

    def extraer_homepage():
        a = soup.find('a', string="Homepage")
        if a and a.get("href"):
            return a.get("href").strip()
        return None

    def extraer_widget_html():
        input_tag = soup.find('input', {'id': 'embed_code'})
        if input_tag and input_tag.get("value"):
            return input_tag["value"]
        return None


    datos = {
        "website": extraer_homepage(),
        "h_index": extraer_h_index(),
        "subject_area": None,  # Este campo no está en esa parte visible
        "publisher": buscar_con_h2("Publisher"),
        "issn": buscar_con_h2("ISSN"),
        "widget": extraer_widget_html() or "No dispobinle",
        "publication_type": buscar_con_h2("Publication type")
    }

    return datos


def obtener_info_revista(nombre_revista):
    print(f"\nProcesando revista: {nombre_revista}")
    url_revista = buscar_url_revista(nombre_revista)
    print(f"URL final encontrada: {url_revista}")

    if not url_revista:
        print(f"No se encontró la revista: {nombre_revista}")
        return None

    time.sleep(5)
    datos = scrap_datos_revista(url_revista)

    if datos:
        print(f"Datos obtenidos correctamente de: {nombre_revista}")
    else:
        print(f"Falló la extracción de datos para: {nombre_revista}")

    return datos
