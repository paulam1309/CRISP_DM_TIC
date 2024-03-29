# -*- coding: utf-8 -*-
"""Taller_Modelado_Evaluacion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1conCZ9KqbWZKrngHlnBjF_-V1w4Tp518
"""

#Taller Modelado y Evaluación TICS en salud
#Paula Sofía Muñoz
import pandas as pd

from imblearn.under_sampling import NearMiss
from collections import Counter

pip install lazypredict

import lazypredict

from lazypredict.Supervised import LazyClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount("/content/drive/")

data_disease=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/new_model (1).csv")
print (data_disease)

X= data_disease[['Htn', 'Sg', 'Rbcc', 'Hemo', 'Al']]
X

Y= data_disease['Class']
Y

us=NearMiss(sampling_strategy='auto', n_neighbors=3, version=2)

"""# Caso 1: Primero se separa los datos en entrenamiento y testeo, luego se hace undersampling:"""

#Separación de datos
X_train, X_test, Y_train, Y_test = train_test_split(X, Y,test_size=.2,random_state =42,stratify=Y)

#Undersampling
X_train_res,Y_train_res =us.fit_resample(X_train,Y_train)
X_test_res, Y_test_res= us.fit_resample(X_test,Y_test)
print('Para entrenamiento:')
print('Antea de la depuración:{}'.format(Counter(Y_train)))
print('Después de la depuración:{}'.format(Counter(Y_train_res)))
print('Antea de la depuración:{}'.format(Counter(X_train)))
print('Después de la depuración:{}'.format(Counter(X_train_res)))

print('Para evaluación:')
print('Antea de la depuración:{}'.format(Counter(Y_test)))
print('Después de la depuración:{}'.format(Counter(Y_test_res)))
print('Antea de la depuración:{}'.format(Counter(X_test)))
print('Después de la depuración:{}'.format(Counter(X_test_res)))

"""# Segundo Caso: se hace primero undersampling, para posteriormente separar los datos en testeo y entrenamiento"""

Xu, Yu =us.fit_resample(X,Y)
print('Antea de la depuración:{}'.format(Counter(Y)))
print('Después de la depuración:{}'.format(Counter(Yu)))
print('Antea de la depuración:{}'.format(Counter(X)))
print('Después de la depuración:{}'.format(Counter(Xu)))

X_train_ru, X_test_ru, Y_train_ru, Y_test_ru = train_test_split(Xu, Yu, test_size=0.2, random_state=42, stratify=Yu)

print('Se usarán de la siguiente manera los datos')
print('Para entrenamiento:{}'.format(Counter(Y_train_ru)))
print('Para testeo:{}'.format(Counter(Y_test_ru)))

"""# Lazy Classifier para ambos modelos:"""

#Primero modelo: primero se divide los datos y se hace undersampling_
clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
models,predictions = clf.fit(X_train_res, X_test_res, Y_train_res, Y_test_res)

print(models)

#Segundo modelo: primero se hace undersampling y luego se dividen los datos
clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
models_2,predictions_2 = clf.fit(X_train_ru,X_test_ru, Y_train_ru, Y_test_ru)

print(models_2)

#Con los datos originales, divididos:
models_3,predictions_3 = clf.fit(X_train, X_test, Y_train, Y_test )
print(models_3)

"""# Prueba de Optimizacion de los Algoritmos

**Bernulli**

Se utiliza principalmente para problemas de clasificación binaria, donde cada característica es una variable booleana (0 o 1), puede no ser la mejor opción para todos los tipos de datos, especialmente si las características no siguen una distribución de Bernoulli o si hay dependencias significativas entre las características.
"""

from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
# Crear el clasificador
bernoulli_nb = BernoulliNB()

bernoulli_nb.fit(X_train_res, Y_train_res)
# Realizar predicciones en el conjunto de prueba
predictions = bernoulli_nb.predict(X_test_res)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test_res, predictions)
print("Accuracy: {:.2f}%".format(accuracy * 100))

print("Classification Report:")
print(classification_report(Y_test_res, predictions))

"""**Ridge Classifier**

La regresión Ridge es una técnica de regularización que agrega una penalización a los coeficientes del modelo para evitar el sobreajuste.
Aquí hay algunas características clave del RidgeClassifier:

Tuning de Hiperparámetros: Puedes ajustar el hiperparámetro de regularización alpha para controlar el equilibrio entre ajustar los datos de entrenamiento y evitar el sobreajuste. Se mira en escala logarítmica (0.1, 1.0, 10.0).
El valor predeterminado de alpha en RidgeClassifier es 1.0

Efecto de alpha:

-Un alpha más pequeño permite que los coeficientes del modelo sean más grandes, lo que puede resultar en un modelo que se ajusta más a los datos de entrenamiento.

-Un alpha más grande impone una penalización más fuerte a los coeficientes, lo que puede ayudar a prevenir el sobreajuste.
"""

from sklearn.linear_model import RidgeClassifierCV

# Crear el clasificador Ridge con búsqueda automática de alpha
ridge_classifier = RidgeClassifierCV(alphas=[0.1, 1.0, 10.0], cv=3)  # Puedes ajustar los valores de alpha según sea necesario

# Entrenar el clasificador
ridge_classifier.fit(X_train_res, Y_train_res)

# Obtener el mejor valor de alpha encontrado durante la búsqueda
best_alpha = ridge_classifier.alpha_
print("Mejor valor de alpha:", best_alpha)

from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Crear el clasificador
ridge_classifier = RidgeClassifier(alpha=0.1)  # Puedes ajustar el valor de alpha según sea necesario

# Entrenar el clasificador
ridge_classifier.fit(X_train_res, Y_train_res)

# Realizar predicciones en el conjunto de prueba
predictions = ridge_classifier.predict(X_test_res)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test_res, predictions)
print("Accuracy: {:.2f}%".format(accuracy * 100))

"""**DummyClassifier:**
strategy="uniform" indica que el clasificador generará predicciones aleatorias.

Este código utiliza la estrategia "most_frequent", que predice siempre la clase mayoritaria en el conjunto de entrenamiento.
"""

from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Crear el DummyClassifier con estrategia aleatoria
dummy_classifier = DummyClassifier()

# Entrenar el clasificador
dummy_classifier.fit(X_train_res, Y_train_res)

# Realizar predicciones en el conjunto de prueba
predictions_random = dummy_classifier.predict(X_test_res)

# Evaluar la precisión del modelo
accuracy_random = accuracy_score(Y_test_res, predictions_random)
print("Accuracy con estrategia aleatoria: {:.2f}%".format(accuracy_random * 100))

from sklearn.model_selection import GridSearchCV
# Definición conjuntp de hiperparámetros que se van a probar
parametro_dummy = {'strategy': ["stratified", "most_frequent", "uniform", "constant"]}

# Inicialización de GridSearchCV
grid_search_dummy = GridSearchCV(dummy_classifier, parametro_dummy, cv=5, scoring='accuracy') #cv=5 significa 5-fold cross-validation

# Búsqueda de hiperparámetros
grid_search_dummy.fit(X_train_res, Y_train_res)

print("Mejores hiperparámetros:", grid_search_dummy.best_params_) # con best_params_ se seleccionan los mejores parametros

# Predicción para el X test
y_pred_dummy= grid_search_dummy.predict(X_test_res)

accuracy_dummy=accuracy_score(Y_test_res, y_pred_dummy)
print(f"Precisión del modelo: {accuracy_dummy}")

# Estrategia de predecir la clase mayoritaria
dummy_classifier_majority = DummyClassifier(strategy="most_frequent")
dummy_classifier_majority.fit(X_train_res, Y_train_res)
predictions_majority = dummy_classifier_majority.predict(X_test_res)
accuracy_majority = accuracy_score(Y_test_res, predictions_majority)
print("Accuracy con estrategia de clase mayoritaria: {:.2f}%".format(accuracy_majority * 100))

"""El que strategy dice como predecirá el clasificador, como se puede ver mejor predice de forma uniforme que indica que el clasificador generará predicciones aleatorias."""

from sklearn.linear_model import RidgeClassifierCV
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import numpy as np


# Crear el RidgeClassifierCV
ridge_classifier_cv = RidgeClassifierCV(alphas=np.arange(0.1, 10, 0.1), cv=5)

# Entrenar el RidgeClassifierCV
ridge_classifier_cv.fit(X_train_res, Y_train_res)

# Realizar predicciones en el conjunto de prueba
y_pred = ridge_classifier_cv.predict(X_test_res)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test_res, y_pred)
print("Precisión del modelo: {:.2f}%".format(accuracy * 100))

# También puedes imprimir otras métricas de evaluación si lo deseas
print("Classification Report:")
print(classification_report(Y_test_res, y_pred))

# Optimizar hiperparámetros si es necesario
param_grid = {'alphas': [np.arange(0.1, 1, 0.1), np.arange(1, 10, 1)]}
grid_search = GridSearchCV(RidgeClassifierCV(cv=5), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_res, Y_train_res)

# Imprimir los mejores hiperparámetros encontrados
print("Mejores hiperparámetros:", grid_search.best_params_)

# Realizar predicciones con el modelo optimizado
y_pred_optimized = grid_search.predict(X_test_res)

# Evaluar la precisión del modelo optimizado
accuracy_optimized = accuracy_score(Y_test_res, y_pred_optimized)
print("Precisión del modelo optimizado: {:.2f}%".format(accuracy_optimized * 100))

"""**LinearDiscriminantAnalysis**
El algoritmo Linear Discriminant Analysis (LDA) es un método de clasificación que busca encontrar las direcciones (discriminantes lineales) que maximizan la separación entre las clases en los datos.

- solver (predeterminado='svd'):
Especifica el algoritmo a utilizar para la optimización. Las opciones incluyen 'svd' para descomposición de valores singulares, 'lsqr' para cuadrados mínimos y 'eigen' para descomposición de eigenvalues. 'eigen' solo es válido si se establece shrinkage en 'auto'.


- shrinkage (predeterminado=None):
Controla la aplicación de la regularización de Shrinkage. Puede ser None (sin regularización), 'auto' (utiliza una heurística para elegir automáticamente entre 'lsqr' o 'eigen') o un valor entre 0 y 1 que controla la cantidad de regularización.

"""

#LinearDiscriminantAanalysis

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report


# Crear el LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis()

# Entrenar el modelo LDA
lda.fit(X_train_res, Y_train_res)

# Realizar predicciones en el conjunto de prueba
y_pred = lda.predict(X_test_res)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test_res, y_pred)
print("Precisión del modelo: {:.2f}%".format(accuracy * 100))

# También puedes imprimir otras métricas de evaluación si lo deseas
print("Classification Report:")
print(classification_report(Y_test_res, y_pred))

# Optimizar hiperparámetros si es necesario
param_grid = {'solver': ['svd', 'lsqr', 'eigen']}
grid_search = GridSearchCV(LinearDiscriminantAnalysis(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_res, Y_train_res)

# Imprimir los mejores hiperparámetros encontrados
print("Mejores hiperparámetros:", grid_search.best_params_)


# Realizar predicciones con el modelo optimizado
y_pred_optimized = grid_search.predict(X_test_res)

# Evaluar la precisión del modelo optimizado
accuracy_optimized = accuracy_score(Y_test_res, y_pred_optimized)
print("Precisión del modelo optimizado: {:.2f}%".format(accuracy_optimized * 100))

"""**Nearest Centroid**
El algoritmo Nearest Centroid es un clasificador que asigna las muestras a la clase cuyo centroide (media) es el más cercano.

shrink_threshold-->controla la magnitud mínima de la inversa del cuadrado de la distancia euclidiana que los centroides deben alcanzar antes de que se realice una regularización.

- shrink_threshold: float or None, default=None
Si es None, no se aplica regularización.
Si es un valor float, la regularización se aplicará para aquellos centroides cuyas distancias al cuadrado sean más pequeñas que shrink_threshold.
Valores más altos de shrink_threshold conducen a una mayor regularización.

-El parámetro metric permite especificar la métrica utilizada para calcular las distancias entre puntos. Algunas de las opciones comunes incluyen:

'euclidean': La distancia euclidiana estándar.
'manhattan' o 'l1': La distancia de Manhattan.
'chebyshev' o 'linf': La distancia de Chebyshev (máxima diferencia a lo largo de todas las dimensiones).
'cosine': La similitud del coseno.
"""

#Nearest Centroid
from sklearn.neighbors import NearestCentroid
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report



# Crear el NearestCentroid
nearest_centroid = NearestCentroid(metric='cosine')

# Entrenar el modelo NearestCentroid
nearest_centroid.fit(X_train_res, Y_train_res)

# Realizar predicciones en el conjunto de prueba
y_pred = nearest_centroid.predict(X_test_res)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test_res, y_pred)
print("Precisión del modelo: {:.2f}%".format(accuracy * 100))

# También puedes imprimir otras métricas de evaluación si lo deseas
print("Classification Report:")
print(classification_report(Y_test_res, y_pred))

# Optimizar hiperparámetros si es necesario
param_grid = {'shrink_threshold': [None, 0.1, 0.5, 1.0]}
grid_search = GridSearchCV(NearestCentroid(), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_res, Y_train_res)

# Imprimir los mejores hiperparámetros encontrados
print("Mejores hiperparámetros:", grid_search.best_params_)

# Realizar predicciones con el modelo optimizado
y_pred_optimized = grid_search.predict(X_test_res)

# Evaluar la precisión del modelo optimizado
accuracy_optimized = accuracy_score(Y_test_res, y_pred_optimized)
print("Precisión del modelo optimizado: {:.2f}%".format(accuracy_optimized * 100))