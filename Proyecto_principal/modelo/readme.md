# Cambios realizados por Andrés David Estrada
Se hizo un modelo supervisado a travez de los datos corregidos que me entregó santiago, solo se usaran las columnas que nos llegan a servir las cuales son:

| columna                 |
| ----------------------- |
| Año                     |
| Índice dedependencia    |
| Índice deenvejecimiento |
| Índice deinfancia       |
| Índice dejuventud       |
| Índice de vejez         |
| Población Total         |

a travez del siguiente codigo:
```
df = pd.read_csv("archivo_corregido.csv",encoding="UTF-8")
print(df.head(),"\n")

df= df[['Año','Índice dedependencia','Índice deenvejecimiento','Índice deinfancia','Índice dejuventud',
        'Índice de vejez', 'Población Total']]
```
## decicion
Decidí solo tomar estas variables debido a que el resto de variables no nos ayudaban para hacer la prediccion, es decir solo tome como variables X's a los indices como vejez para calcular la población total a travez de la predicción (variable Y)\\
Esto por facilidad del proyecto ya que tendriamos que hacer varias predicciones lo que puede dificultar el codigo de api.py y templates.html

## entrenamiento de modelo
el entrenamiento del modelo se realiza a travez del siguiente codigo
```

x=df.drop(columns=['Población Total'])
y=df['Población Total']
#codificar variables categoricas
x_encoded= pd.get_dummies(x)


x_train,x_test,y_train,y_test= train_test_split(x_encoded,y,test_size=0.2,random_state=42)

modelo=LinearRegression()
modelo.fit(x_train,y_train)
with open('modelo.pkl',"wb") as f:
    pickle.dump(modelo,f)
with open('columnas.pkl','wb') as f:
    pickle.dump(x_encoded.columns.tolist(),f)
```
\\
esto generará dos archivos que son los 
modelo.txt
columnas.txt 

estos se encontraran en mi carpeta y son muy importantes para la creacion del codigo templates.html y api.py



