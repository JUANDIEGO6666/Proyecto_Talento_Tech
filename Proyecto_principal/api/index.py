# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for
import pickle
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")
TEMPLATES_DIR = os.path.abspath(TEMPLATES_DIR)
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
STATIC_DIR = os.path.abspath(STATIC_DIR)

# Aquí ajustamos para que busque en la carpeta ../modelo
MODELO_DIR = os.path.join(BASE_DIR, "..", "modelo")
MODELO_DIR = os.path.abspath(MODELO_DIR)

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

with open(os.path.join(MODELO_DIR, "modelo.pkl"), "rb") as f:
    modelo = pickle.load(f)
with open(os.path.join(MODELO_DIR, "columnas.pkl"), "rb") as f:
    columnas = pickle.load(f)

@app.route("/", methods=["GET"])
def formulario():
    anos = list(range(1985, 2036))
    porcentajes = list(range(0, 101, 10))
    return render_template("formulario.html", anos=anos, porcentajes=porcentajes)

@app.route("/predecir", methods=["POST"])
def predecir():
    ano = int(request.form.get("ano"))
    tipo_poblacion = request.form.get("tipo_poblacion")
    genero_pred = request.form.get("genero_pred")
    dep = float(request.form.get("dep"))
    enve = float(request.form.get("enve"))
    nin = float(request.form.get("nin"))

    datos = {
        "Año": ano,
        "Índice de dependencia": dep,
        "Índice de envejecimiento": enve,
        "Índice de infancia": nin,
        "Tipo población urbana": 1 if tipo_poblacion == "Urbana" else 0,
        "Género predominante mujeres": 1 if genero_pred == "Mujeres" else 0,
    }

    df = pd.DataFrame([datos])
    df = df.reindex(columns=columnas, fill_value=0)

    prediccion = float(modelo.predict(df)[0])
    prediccion_int = int(round(prediccion))
    prediccion_fmt = f"{prediccion_int:,}".replace(",", ".")

    return render_template("resultado.html", prediccion=prediccion_fmt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
