# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for
import pickle
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "..", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")
MODELO_DIR = os.path.join(BASE_DIR, "..", "modelo")

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Cargar modelo y columnas
with open(os.path.join(MODELO_DIR, "modelo.pkl"), "rb") as f:
    modelo = pickle.load(f)
with open(os.path.join(MODELO_DIR, "columnas.pkl"), "rb") as f:
    columnas = pickle.load(f)

# Agregamos columnas extras al final, si no existen
if "Tipo de población" not in columnas:
    columnas.append("Tipo de población")
if "Género predominante" not in columnas:
    columnas.append("Género predominante")

@app.route("/", methods=["GET"])
def formulario():
    return render_template("formulario.html", columnas=columnas)

@app.route("/predecir", methods=["POST"])
def predecir():
    datos = {}
    for col in columnas:
        valor = request.form.get(col)
        try:
            datos[col] = float(valor)
        except:
            datos[col] = 0  # Si no hay valor, se pone 0 por defecto

    df = pd.DataFrame([datos])
    # Reordenar con columnas del modelo original (ignorando las extras)
    df_modelo = df.reindex(columns=columnas, fill_value=0)

    prediccion = float(modelo.predict(df_modelo[columnas[:-2]])[0])  # modelo no usa las extras
    prediccion_int = int(round(prediccion))
    prediccion_fmt = f"{prediccion_int:,}".replace(",", ".")

    return render_template("resultado.html", prediccion=prediccion_fmt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

