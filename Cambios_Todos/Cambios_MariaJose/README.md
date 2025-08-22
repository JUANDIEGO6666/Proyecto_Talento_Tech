# 🌎 Proyecto: Predicción de Población en Manizales (1985–2035)

Este proyecto es una aplicación web en **Flask** que permite predecir la población total de Manizales usando indicadores demográficos históricos.  
El sistema se compone de **modelo de predicción**, **backend**, **interfaz web** y **estilos visuales**.

---

## 🎨 Estilos: `static/style.css`

El archivo `style.css` define la apariencia visual de la aplicación.  
Sus características principales:

- **Fondo moderno**: degradado azul oscuro → celeste.
- **Animación fade-in**: hace que los formularios y páginas aparezcan suavemente.
- **Tarjetas** (`.card`): cuadros blancos con bordes redondeados y sombra para resaltar el contenido.
- **Formulario responsivo**:  
  - Distribuido en una cuadrícula de 3 columnas en pantallas grandes.  
  - Se adapta a 1 columna en pantallas pequeñas (móviles).
- **Inputs estilizados**: selects y cajas con bordes suaves, efecto de enfoque (focus) iluminado.
- **Botones personalizados**:  
  - **Azul primario** con hover más oscuro.  
  - **Secundario** blanco para el botón de volver.

> El objetivo es que la aplicación se vea **limpia, moderna y fácil de usar**.

---

## 📝 Formulario: `templates/formulario.html`

Es la página principal de la aplicación.  
Aquí el usuario ingresa los datos necesarios para generar la predicción.

Campos disponibles:

- **Año** → desplegable de 1985 a 2035.  
- **Tipo de población** → Urbano / Rural.  
- **Género predominante** → Mujeres / Hombres.  
- **Dependencia poblacional (%)** → opciones en saltos de 10%.  
- **Adultos mayores (%)** → opciones en saltos de 10%.  
- **Niñez (%)** → opciones en saltos de 10%.  

Al final, un gran botón azul: **“Predecir Población”**.

> Cuando se envía, Flask recoge los valores y calcula la predicción usando el modelo entrenado.

---

## 📊 Resultado: `templates/resultado.html`

Después de enviar el formulario, el usuario llega a esta página.  
Muestra:

- Un mensaje con la predicción:  
  **“La población estimada es: 350.000 habitantes”**
- Un botón secundario: **“Volver”**, que redirige al formulario para hacer otra predicción.

El diseño mantiene la misma estética: tarjeta blanca centrada, texto claro y botón estilizado.

---

##  Procedimiento

1. El usuario abre el **formulario**.  
2. Ingresa los datos demográficos y selecciona el año.  
3. Presiona **“Predecir Población”**.  
4. Flask procesa la solicitud, usa el **modelo entrenado** y calcula la predicción.  
5. Se muestra el **resultado** en pantalla.

---
## CAMBIOS EN INDEX Y MODELO
# 🛠️ Explicación de los Cambios en `modelo.py` y `index.py`

Este documento describe de manera clara y humanizada los **cambios realizados** en los archivos principales del proyecto para asegurar que el **modelo de predicción** y la **aplicación web** funcionen de forma coherente con el dataset y el formulario.

---

## 🔹 Cambios en `modelo.py`

### 📍 Contexto
El **CSV** que usamos contiene columnas como:
- Población urbana
- Población rural
- Población total hombres
- Población total mujeres

Pero el **formulario web** le pide al usuario datos más simples:
- Tipo de población (Urbana / Rural)
- Género predominante (Mujeres / Hombres)

Si usábamos el CSV sin cambios, el formulario tendría campos que el modelo no entendería.

---

### ✅ Solución
Se **crearon nuevas variables binarias** a partir de la información del CSV:

```python
# Tipo de población (1 = urbana, 0 = rural)
if col_urb and col_rur:
    X["Tipo población urbana"] = (df[col_urb] >= df[col_rur]).astype(int)
else:
    X["Tipo población urbana"] = 0

# Género predominante (1 = mujeres, 0 = hombres)
if col_hom and col_muj:
    X["Género predominante mujeres"] = (df[col_muj] >= df[col_hom]).astype(int)
else:
    X["Género predominante mujeres"] = 0
