#Se importan las librerias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle

#Creamos una variable y usamos pd.read para leer los datos

ruta= Path('Cambios_Todos')/'archivo.csv'
demografico = pd.read_csv('C:/Users/User/Desktop/IA_pr2/Proyecto_Talento_Tech/archivo.csv')

#Compruebo la lectura del archvio csv e imprimo las primeras 10 filas
print("________________________________Datos_____________________________________")
print(demografico.head(),"\n")
#usando el "\n" se hace un salto de linea 
#Diagrama de la población a medida de los años

print("Estaditicas")
print(demografico.describe())     # Estadísticas básicas

plt.figure(figsize=(15,10))
sns.boxplot(x='Año',y='Población Total',data=demografico,palette= 'Set2')
plt.title("Incremento de población por año")
plt.xlabel("Año")
plt.ylabel("población")
plt.show()

#Como tenemos tantos valores, entonces vamos a elegir un valor si y un valor no, Esto para hacer mas pequeña las filas

demografico = demografico.iloc[::2]  # Esto toma una fila sí y una no

plt.figure(figsize=(15,10))
sns.boxplot(x='Año',y='Población Total',data=demografico,palette= 'Set2')
plt.title("Incremento de población por año")
plt.xlabel("Año")
plt.ylabel("población")
plt.show()


data = pd.read_csv('C:/Users/User/Desktop/IA_pr2/Proyecto_Talento_Tech/archivo.csv')
df =pd.DataFrame(data)
# separar variables
x= df.drop(columns='Población Total')
y= df['Población Total']
# codificar variables categóricas
x_encoded=pd.get_dummies(x)
#print(x_encoded)
# Dividir datos
x_train,x_test,y_train,y_test=train_test_split(x_encoded,y,test_size=0.2,random_state=42)
# Entrenar modelo
modelo=LinearRegression()
modelo.fit(x_train,y_train)
# Guardar modelo
with open('modelo.pkl','wb') as f:
    pickle.dump(modelo,f)
with open('columnas.pkl','wb') as f:
    pickle.dump(x_encoded.columns.tolist(),f)

df = demografico.copy()
x = df.drop(columns='Población Total')
y = df['Población Total']
...

df = demografico.copy()
x = df.drop(columns='Población Total')
y = df['Población Total']

df.to_csv('archivo_corregido.csv', index=False)