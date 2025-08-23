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

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# Cargar modelo y columnas originales
with open(os.path.join(MODELO_DIR, "modelo.pkl"), "rb") as f:
    modelo = pickle.load(f)
with open(os.path.join(MODELO_DIR, "columnas.pkl"), "rb") as f:
    columnas = pickle.load(f)

# ADICIÓN: columnas extra SOLO para la interfaz
columnas_extra = ["Tipo de población", "Género predominante"]
for c in columnas_extra:
    if c not in columnas:
        columnas.append(c)

# ADICIÓN: columnas que REALMENTE vio el modelo (sin las extra)
columnas_modelo = [c for c in columnas if c not in columnas_extra]

@app.route("/", methods=["GET"])
def formulario():
    anos = list(range(1985, 2036))
    return render_template("formulario.html", columnas=columnas, anos=anos)

@app.route("/predecir", methods=["POST"])
def predecir():
    datos = {}
    # Cargamos todo lo que venía del formulario EXCEPTO las extra
    for col in columnas:
        if col in columnas_extra:
            continue  # estas no van directo al modelo
        valor = request.form.get(col)
        try:
            datos[col] = float(valor)
        except:
            datos[col] = 0

    df = pd.DataFrame([datos])
    # Aseguramos el orden y que sólo estén las columnas del modelo
    df = df.reindex(columns=columnas_modelo, fill_value=0)

    # --- ADICIÓN OPCIONAL ---
    # Si el usuario escogió tipo de población o género, los calculamos (no afectan al modelo)
    tipo_poblacion = request.form.get("tipo_poblacion")
    genero_pred = request.form.get("genero_pred")
    if tipo_poblacion:
        df["Tipo de población"] = 1 if tipo_poblacion == "Urbana" else 0
    if genero_pred:
        df["Género predominante"] = 1 if genero_pred == "Mujeres" else 0

    # MUY IMPORTANTE: sólo pasamos al modelo lo que vio en el ajuste
    X_pred = df[columnas_modelo]
    prediccion = float(modelo.predict(X_pred)[0])
    prediccion_int = int(round(prediccion))
    prediccion_fmt = f"{prediccion_int:,}".replace(",", ".")

    return render_template("resultado.html", prediccion=prediccion_fmt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
