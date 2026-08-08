# Experimento de Nudos Aleatorios

Proyecto de matemática experimental para estudiar la distribución
de tipos de nudo producida por polígonos cerrados equidistantes
aleatorios en R³.

## Pregunta principal

Para un número N de segmentos queremos estimar:

p_N(K) = P(K | N)

donde K representa un tipo de nudo.

Posteriormente queremos estudiar la probabilidad de que dos polígonos
independientes representen el mismo tipo de nudo:

C_(N,M) = Σ p_N(K) p_M(K)

y, para el mismo número de segmentos:

C_(N,N) = Σ p_N(K)²

---

## Modelo geométrico

Cada muestra es un polígono cerrado formado por N segmentos.

Todos los segmentos tienen la misma longitud:

|v_i| = L

y el último segmento conecta nuevamente el último vértice con el primero.

El número N representa el número de segmentos del polígono.

NO representa el crossing number del nudo.

---

## Generación

La primera implementación utiliza Topoly para generar loops
poligonales equidistantes.

La generación está separada de la clasificación topológica para
permitir sustituir posteriormente el algoritmo si necesitamos
comparar distintos modelos de muestreo.

---

## Clasificación

La primera clasificación utiliza el polinomio de Alexander mediante
Topoly.

Esto NO debe interpretarse todavía como una demostración de equivalencia
topológica para cualquier par de nudos.

Los invariantes son herramientas para distinguir nudos, pero un mismo
invariante puede ser compartido por nudos no equivalentes.

Por tanto, durante las primeras fases registraremos también los casos
que el clasificador no pueda identificar.

---

## Flujo experimental

```text
polígono cerrado aleatorio
          |
          v
validación geométrica
          |
          v
curva espacial
          |
          v
invariante topológico
          |
          v
tipo de nudo
          |
          v
conteo
          |
          v
p_N(K)