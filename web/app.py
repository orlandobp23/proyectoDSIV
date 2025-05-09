'''Programa principal de MovieDB'''
from flask import Flask, request, url_for , render_template, redirect, session



app = Flask(__name__)


@app.route('/area')
def areas():
    import json
    with open('web/data/datos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extraer todas las áreas únicas
    areas = set()
    for revista in data.values():
        for a in revista['areas']:
            areas.add(a)

    return render_template('area.html', revistas=data, areas=sorted(areas))

@app.route('/area/<area_nombre>')
def ver_area(area_nombre):
    import json, os
    ruta = os.path.join('web', 'data', 'datos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)

    revistas_filtradas = []
    for nombre, datos in data.items():
        if area_nombre in datos.get('areas', []):
            revistas_filtradas.append((nombre, datos.get('h_index', 'N/A')))

    return render_template('area_resultado.html', area=area_nombre, revistas=revistas_filtradas)

@app.route('/catalogo')
def catalogos():
    import json
    with open('web/data/datos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extraer todas las áreas únicas
    catalogos = set()
    for revista in data.values():
        for a in revista['catalogos']:
            catalogos.add(a)

    return render_template('catalogo.html', revistas=data, catalogos=sorted(catalogos))

@app.route('/catalogo/<catalogo_nombre>')
def ver_catalogo(catalogo_nombre):
    import json, os
    ruta = os.path.join('web', 'data', 'datos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)

    revistas_filtradas = []
    for nombre, datos in data.items():
        if catalogo_nombre in datos.get('catalogos', []):
            revistas_filtradas.append((nombre, datos.get('h_index', 'N/A')))

    return render_template('catalogo_resultado.html', catalogo=catalogo_nombre, revistas=revistas_filtradas)

@app.route('/explorar')
def explorar():
    letras = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return render_template("explorar.html", letras=letras)

@app.route('/explorar/<letra>')
def explorar_letra(letra):
    import json, os
    ruta = os.path.join('web', 'data', 'datos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)

    revistas_filtradas = []
    for nombre, datos in data.items():
        if nombre.upper().startswith(letra.upper()):
            revistas_filtradas.append({
                "nombre": nombre,
                "h_index": datos.get("h_index", "N/A"),
                "areas": datos.get("areas", []),
                "catalogos": datos.get("catalogos", [])
            })

    return render_template("explorar_resultado.html", letra=letra, revistas=revistas_filtradas)




@app.route('/revista/<nombre>')
def detalle_revista(nombre):
    import json, os
    ruta = os.path.join('web', 'data', 'datos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)

    revista = data.get(nombre.lower())
    if not revista:
        return f"No se encontró información para: {nombre}", 404

    return render_template('revista_detalle.html', nombre=nombre, revista=revista)




   


@app.route('/')
def index():
    '''Página principal de la aplicación'''
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    