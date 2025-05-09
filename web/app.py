'''Programa principal de MovieDB'''
from flask import Flask, request, url_for , render_template, redirect, session
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash
import json, os
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.secret_key = 'atlascientifico_2025_login_seguro'


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

from collections import defaultdict

@app.route('/explorar')
def explorar():
    import json, os
    ruta = os.path.join('web', 'data', 'datos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)

    letras = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    conteo = defaultdict(int)
    for nombre in data:
        inicial = nombre[0].upper()
        if inicial.isalpha():
            conteo[inicial] += 1

    return render_template("explorar.html", letras=letras, conteo=conteo)


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

@app.route('/busqueda')
def busqueda():
    import json, os
    q = request.args.get('q', '').strip()
    resultados = []

    if q:
        palabras = q.lower().split()
        ruta = os.path.join('web', 'data', 'datos.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for nombre, datos in data.items():
            nombre_l = nombre.lower()
            if any(palabra in nombre_l for palabra in palabras):  # operación de UNIÓN
                resultados.append({
                    "nombre": nombre,
                    "h_index": datos.get("h_index", "N/A"),
                    "areas": datos.get("areas", []),
                    "catalogos": datos.get("catalogos", [])
                })

    return render_template('busqueda.html', q=q, resultados=resultados)


@app.route('/creditos')
def creditos():
    import json, os
    ruta = os.path.join('web', 'data', 'creditos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('creditos.html', creditos=data)



@app.route('/revista/<nombre>')
def detalle_revista(nombre):
    import json, os

    ruta_datos = os.path.join('web', 'data', 'datos.json')
    with open(ruta_datos, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Buscar la revista sin depender de mayúsculas/minúsculas
    nombre_real = None
    for key in data.keys():
        if key.lower() == nombre.lower():
            nombre_real = key
            break

    if not nombre_real:
        return "Revista no encontrada", 404

    revista = data[nombre_real]

    es_favorita = False
    if 'usuario' in session:
        ruta_fav = os.path.join('web', 'data', 'favoritos.json')
        if os.path.exists(ruta_fav):
            with open(ruta_fav, 'r', encoding='utf-8') as f:
                favoritos = json.load(f)
            es_favorita = nombre_real in favoritos.get(session['usuario'], [])

    return render_template('revista_detalle.html',
                           nombre=nombre_real,
                           revista=revista,
                           es_favorita=es_favorita)





@app.route('/login', methods=['GET', 'POST'])
def login():
    ruta = os.path.join('web', 'data', 'usuarios.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        usuarios = json.load(f)

    error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        if usuario in usuarios:
            hash_guardado = usuarios[usuario]['password']
            if check_password_hash(hash_guardado, password):
                session['usuario'] = usuario
                session['nombre'] = usuarios[usuario]['nombre']
                return redirect(url_for('index'))

        error = 'Credenciales incorrectas'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/usuarios')
def usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('usuarios.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    import json, os
    ruta = os.path.join('web', 'data', 'usuarios.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        usuarios = json.load(f)
        error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        nombre = request.form['nombre']

        if usuario in usuarios:
            error = 'El usuario ya existe'
        else:
            usuarios[usuario] = {
                "password": generate_password_hash(password),
                "nombre": nombre
            }
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)

            session['usuario'] = usuario
            session['nombre'] = nombre
            return redirect(url_for('index'))


    return render_template('registro.html', error=error)

@app.route('/favorito/<nombre>', methods=['POST'])
def toggle_favorito(nombre):
    from urllib.parse import unquote
    nombre = unquote(nombre)

    if 'usuario' not in session:
        return {'status': 'unauthorized'}, 401

    import json, os
    ruta_datos = os.path.join('web', 'data', 'datos.json')
    with open(ruta_datos, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Buscar clave real sin importar mayúsculas
    nombre_real = None
    for key in data:
        if key.lower() == nombre.lower():
            nombre_real = key
            break

    if not nombre_real:
        return {'status': 'not_found'}, 404

    ruta_fav = os.path.join('web', 'data', 'favoritos.json')
    if not os.path.exists(ruta_fav):
        with open(ruta_fav, 'w', encoding='utf-8') as f:
            json.dump({}, f)

    with open(ruta_fav, 'r', encoding='utf-8') as f:
        favoritos = json.load(f)

    usuario = session['usuario']
    favoritos.setdefault(usuario, [])

    if nombre_real in favoritos[usuario]:
        favoritos[usuario].remove(nombre_real)
        estado = 'removed'
    else:
        favoritos[usuario].append(nombre_real)
        estado = 'added'

    with open(ruta_fav, 'w', encoding='utf-8') as f:
        json.dump(favoritos, f, indent=4, ensure_ascii=False)

    return {'status': estado}

@app.route('/mis-favoritos')
def mis_favoritos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    import json, os
    ruta_favs = os.path.join('web', 'data', 'favoritos.json')
    ruta_datos = os.path.join('web', 'data', 'datos.json')

    if not os.path.exists(ruta_favs):
        favoritos = {}
    else:
        with open(ruta_favs, 'r', encoding='utf-8') as f:
            favoritos = json.load(f)

    with open(ruta_datos, 'r', encoding='utf-8') as f:
        data = json.load(f)

    favoritas = favoritos.get(session['usuario'], [])
    revistas_favoritas = []

    for nombre in favoritas:
        if nombre in data:
            revista = data[nombre]
            revistas_favoritas.append({
                "nombre": nombre,
                "h_index": revista.get("h_index", "N/A"),
                "areas": revista.get("areas", []),
                "catalogos": revista.get("catalogos", [])
            })

    return render_template('favoritos.html', revistas=revistas_favoritas)


   


@app.route('/')
def index():
    '''Página principal de la aplicación'''
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    