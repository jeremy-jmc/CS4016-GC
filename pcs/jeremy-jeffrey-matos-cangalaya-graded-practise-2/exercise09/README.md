# Voronoi y Delaunay

## Diagrama de Voronoi

El diagrama de Voronoi es una partición del espacio en regiones basadas en la distancia a un conjunto específico de puntos, también llamados semillas, sitios o generadores. Cada región es un polígono convexo que contiene exactamente una semilla, y cualquier punto dentro de un polígono está más cerca de su semilla que de cualquier otra.

## Triangulación de Delaunay

La triangulación de Delaunay es una subdivisión de un conjunto de puntos en el plano euclidiano, donde para cada triángulo de la triangulación, el círculo circunscrito a dicho triángulo no contiene ningún otro punto del conjunto.

## Cálculo de la triangulación de Delaunay

La triangulación de Delaunay se puede calcular utilizando varios algoritmos eficientes, incluyendo:

- Algoritmo de Bowyer-Watson
- Algoritmo de Delaunay DeWall
- Sweephull

## Uso de la triangulación de Delaunay para calcular el diagrama de Voronoi

Dado que el diagrama de Voronoi es el dual de la triangulación de Delaunay, se puede calcular a partir de los siguientes pasos:

1. Calcular la triangulación de Delaunay utilizando uno de los algoritmos mencionados anteriormente.
2. Construir el diagrama de Voronoi basándose en la triangulación de Delaunay. Las aristas del diagrama de Voronoi son perpendiculares a los segmentos que conectan los centros de los círculos circunscritos a cada triángulo de la triangulación de Delaunay.
3. Para calcular las aristas del diagrama de Voronoi, se deben determinar las líneas perpendiculares bisectrices de cada segmento de la triangulación de Delaunay.
4. Luego, se encuentran los puntos de intersección de estas líneas para obtener los vértices del diagrama de Voronoi.
5. Finalmente, las aristas del diagrama de Voronoi son los segmentos que conectan los vértices encontrados en el paso anterior.

## Conclusiones

Los diagramas de Voronoi y la triangulación de Delaunay son herramientas fundamentales en geometría computacional con una amplia variedad de aplicaciones en campos como la cartografía, la computación gráfica, la planificación de redes y más. Su relación dual proporciona una poderosa conexión entre la distribución espacial de puntos y sus regiones circundantes, lo que permite análisis y visualizaciones precisas de datos espaciales.
