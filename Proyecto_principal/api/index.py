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

MODELO_DIR = os.path.join(BASE_DIR, "..", "modelo")
MODELO_DIR = os.path.abspath(MODELO_DIR)


app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Cargar modelo y columnas originales
with open(os.path.join(MODELO_DIR, "modelo.pkl"), "rb") as f:
    modelo = pickle.load(f)
with open(os.path.join(MODELO_DIR, "columnas.pkl"), "rb") as f:
    columnas = pickle.load(f)

# 👉 Agregamos las nuevas columnas al final SOLO para la interfaz
columnas.extend(["Tipo de población", "Género predominante"])

@app.route("/", methods=["GET"])
def formulario():
    # Lista de años para el desplegable
    anos = list(range(1985, 2036))
    return render_template("formulario.html", columnas=columnas, anos=anos)

@app.route("/predecir", methods=["POST"])
def predecir():
    datos = {}
    for col in columnas:
        if col in ["Tipo de población", "Género predominante"]:
            continue  # estas no van al modelo
        valor = request.form.get(col)
        try:
            datos[col] = float(valor)
        except:
            datos[col] = 0

    df = pd.DataFrame([datos])
    df = df.reindex(columns=columnas[:-2], fill_value=0)  # solo columnas del modelo

    prediccion = float(modelo.predict(df)[0])
    prediccion_int = int(round(prediccion))
    prediccion_fmt = f"{prediccion_int:,}".replace(",", ".")

    return render_template("resultado.html", prediccion=prediccion_fmt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

