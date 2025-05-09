import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

BASE_SEARCH_URL = "https://www.scimagojr.com/journalsearch.php?q="

def buscar_url_revista(nombre_revista):
    """
    Devuelve la URL del perfil de la revista desde la página de búsqueda de SCImago.
    """
    query = quote(nombre_revista)
    url_busqueda = BASE_SEARCH_URL + query
    print(f"🔍 Buscando URL de: {nombre_revista}")
    
    try:
        response = requests.get(url_busqueda, timeout=10)
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
        print(f"✓ URL encontrada: {perfil_url}")
        return perfil_url
    else:
        print(f"✗ No se encontró perfil para: {nombre_revista}")
        return None

def scrap_datos_revista(url):
    """
    Extrae información del perfil de la revista desde su página en SCImago.
    """
    print(f"🌐 Accediendo a perfil: {url}")
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        print(f"Error accediendo a {url}: {e}")
        return None

    if response.status_code != 200:
        print(f"Error {response.status_code} al acceder al perfil de la revista")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    def extraer_texto(selector):
        tag = soup.select_one(selector)
        return tag.text.strip() if tag else None

    def extraer_widget_html(selector):
        tag = soup.select_one(selector)
        return str(tag) if tag else None

    datos = {
        "website": extraer_texto('a[target="_blank"]'),
        "h_index": extraer_texto('div.h-index-value'),
        "subject_area": extraer_texto('div#journal_subject_area'),
        "publisher": extraer_texto('div#journalPublisher'),
        "issn": extraer_texto('div#journalIssn'),
        "widget": extraer_widget_html('div#journal_wdiget iframe'),
        "publication_type": extraer_texto('div#journal_type')
    }

    return datos

def obtener_info_revista(nombre_revista):
    """
    Función principal que combina la búsqueda de la URL y el scraping de datos.
    """
    print(f"\n🔎 Procesando revista: {nombre_revista}")
    url_revista = buscar_url_revista(nombre_revista)
    if not url_revista:
        print(f"✗ No se encontró la revista: {nombre_revista}")
        return None

    time.sleep(1)  # Evita saturar SCImago con muchas peticiones rápidas
    datos = scrap_datos_revista(url_revista)
    
    if datos:
        print(f"✓ Datos obtenidos correctamente de: {nombre_revista}")
    else:
        print(f"✗ Falló la extracción de datos para: {nombre_revista}")

    return datos
