import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import unicodedata
import os

def _normalize(s):
    s = s.strip()
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    return s.lower().replace("  ", " ").replace(" ", "_")

def entrenar(csv_path="archivo.csv",
             salida_modelo="modelo/modelo.pkl",
             salida_columnas="modelo/columnas.pkl"):
    df = pd.read_csv(csv_path, encoding="utf-8")
    norm_cols = {_normalize(c): c for c in df.columns}

    # Función auxiliar para encontrar columnas aunque haya variaciones de nombre
    def fetch(key, aliases=None):
        if key in norm_cols:
            return norm_cols[key]
        aliases = aliases or []
        for a in aliases:
            if a in norm_cols:
                return norm_cols[a]
        for k, v in norm_cols.items():
            if k.startswith(key[:8]):
                return v
        raise KeyError(f"No se encontró columna para {key}")

    # Columnas
    col_ano = fetch("ano")
    col_dep = fetch("indice_de_dependencia", ["indice_dedependencia","indice_dependencia"])
    col_enve = fetch("indice_de_envejecimiento", ["indice_deenvejecimiento","indice_envejecimiento"])
    col_inf = fetch("indice_de_infancia", ["indice_deinfancia","indice_infancia"])
    col_urb = norm_cols.get("poblacion_urbana")
    col_rur = norm_cols.get("poblacion_rural")
    col_hom = norm_cols.get("poblacion_total_hombres")
    col_muj = norm_cols.get("poblacion_total_mujeres")
    col_target = fetch("poblacion_total")

    # Variables de entrada
    X = pd.DataFrame({
        "Año": df[col_ano],
        "Índice de dependencia": df[col_dep],
        "Índice de envejecimiento": df[col_enve],
        "Índice de infancia": df[col_inf],
    })

    # Derivadas binarias para que coincidan con el formulario
    if col_urb and col_rur:
        X["Tipo población urbana"] = (df[col_urb] >= df[col_rur]).astype(int)
    else:
        X["Tipo población urbana"] = 0

    if col_hom and col_muj:
        X["Género predominante mujeres"] = (df[col_muj] >= df[col_hom]).astype(int)
    else:
        X["Género predominante mujeres"] = 0

    y = df[col_target]

    # Entrenamiento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression().fit(X_train, y_train)

    # Guardar
    os.makedirs(os.path.dirname(salida_modelo), exist_ok=True)
    with open(salida_modelo, "wb") as f:
        pickle.dump(modelo, f)
    with open(salida_columnas, "wb") as f:
        pickle.dump(list(X.columns), f)

    print("Modelo entrenado y guardado con éxito.")
    print("R² en test:", modelo.score(X_test, y_test))

if __name__ == "__main__":
    entrenar()
