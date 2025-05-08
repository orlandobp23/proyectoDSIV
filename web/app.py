'''Programa principal de MovieDB'''
from flask import Flask, request, url_for , render_template, redirect, session
import os
import random


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para sesiones







   


@app.route('/')
def index():
    '''Página principal de la aplicación'''
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    