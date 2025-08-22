# Proyecto_Talento_Tech - Predicción de densidad poblacional
## Descripción
se realizara un modelo predictivo de maching learning donde los funcionarios encargados de realizar analisis de mercado y densidad demografica de la ciudad de manizales puedan realizar la prediccion de cuantas personas habran en la zona teniendo en cuenta datos como indices de envejecimiento, infantil entre otros
esto ayudara a los funcionarios a tener en cuenta con mayor precision la cantidad de personas que viven en Manizales a la hora de realizar campañas sociales o proyectos
## Librerias para realizar el proyecto
| libreria          |
| ----------------- |
| pickle            |
| pandas            |
| os                |
| matplotlib.pyplot |
| seaborn           |
| pathlib           |
## Pasos para la realizacion del proyecto
### Limpieza de datos 
se realiza una limpieza de todos los datos en el cual se eliminan datos nulos, duplcados, irregulares o ilogicos con el fin de que se haga un entrenamiento correcto del modelo
### Creacion del modelo
Con los datos limpios se realiza el entrenamiento del modelo. Se segmentan datos que se vayan a utilizar como variables X´s como correlacion del dato que queremos predecir (variables Y's)\\
las variables X para este proyecto son:
 * Año
 * Índice dedependencia
 * Índice deenvejecimiento
 * Índice deinfancia
 * Índice dejuventud
 * Índice de vejez
\\
Variable Y:
 * Población total

### Templates
se crea una carpeta Templates donde se creara el front-ent con el cual el usuario funcionario interectuara y pondra los valores con el cual se realizara la predicción
### API
Se crea una carpeta api donde se hace la relacion entre el front-ent y el back-end del modelo predictivo
## Direccion del aplicativo para predicion
**http://192.168.10.19:5000/**