#  Proyecto: Predicción de Población en Manizales (1985–2035)

Este proyecto es una aplicación web en **Flask** que permite predecir la población total de Manizales usando indicadores demográficos históricos.  
El sistema se compone de **modelo de predicción**, **backend**, **interfaz web** y **estilos visuales**.

---

##  Estilos: `static/style.css`

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

##  Formulario: `templates/formulario.html`

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

##  Resultado: `templates/resultado.html`

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

#  Cambios realizados en `modelo.py` y `index.py`

## Cambios en `modelo.py`

### Explicación general
El archivo `modelo.py` originalmente cargaba el CSV y entrenaba un modelo con variables básicas como:
- Año
- Índice de dependencia
- Índice de envejecimiento
- Índice de infancia

Sin embargo, para hacer la predicción más precisa y coherente con el **formulario web**, se decidió **agregar dos nuevas variables** derivadas del dataset:
- **Tipo de población** (urbana o rural)
- **Género predominante** (mujeres o hombres)

###  Código agregado

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
```

## Qué hace este código

**Tipo población urbana** → compara las columnas Población urbana y Población rural del CSV.
Si la urbana es mayor o igual → asigna 1.
Si la rural es mayor → asigna 0.
**Género predominante mujeres** → compara las columnas Población total mujeres y Población total hombres.
Si las mujeres son mayoría → asigna 1.
Si los hombres son mayoría → asigna 0.

De esta forma, el modelo puede usar estos indicadores simplificados y entrenar con ellos.

# Cambios en `index.py`
### Explicación general

El archivo index.py recibe los valores que el usuario elige en el formulario.
Inicialmente manejaba solo las variables originales (año, dependencia, envejecimiento, infancia).

Pero, como en el formulario se piden también Tipo de población y Género predominante, era necesario convertir esas respuestas de texto en las variables binarias que el modelo entrenó.

## Código agregado
"Tipo población urbana": 1 if tipo_poblacion == "Urbana" else 0,
"Género predominante mujeres": 1 if genero_pred == "Mujeres" else 0,

## Qué hace este código

Si el usuario selecciona Urbana en el formulario → el valor será 1.
Si selecciona Rural → el valor será 0.
Si selecciona Mujeres → el valor será 1.
Si selecciona Hombres → el valor será 0.

Así, los datos del formulario coinciden exactamente con lo que espera el modelo entrenado.

##  Conclusión

Antes: el modelo y el backend trabajaban solo con las columnas originales del CSV.

Ahora: se añadieron variables derivadas (tipo de población y género predominante) que hacen que la predicción sea más rica y que el formulario tenga un efecto real en los resultados.

Gracias a estos cambios:
El modelo.py entrena con más información.
El index.py traduce las respuestas del usuario en los mismos términos que entiende el modelo.

Esto garantiza que la aplicación sea más precisa, consistente y útil