# -----------------------------------------------------------------------------
# Voronoi diagram
# ----------------------------------------------------------------------------- 
# Fortune's algorithm

# -----------------------------------------------------------------------------
# Delaunay triangulation
# -----------------------------------------------------------------------------

"""
1. Nro de triangulaciones de un poligono regular
    Tomas una arista y la usas como semilla, trazas todos los posibles triangulos que usen esa arista
    Llamas a la funcion recursiva para los 2 subproblemas que dejas
2. Area de un poligono convexo
    https://cses.fi/problemset/task/2191
    https://www.youtube.com/watch?v=G9QTjWtK_TQ
3. Area de la interseccion de 2 poligonos convexos
    Primero verificas los puntos del poligono 1 que estan dentro del poligono 2 y viceversa
    Luego verificas los segmentos que se intersectan para generar los otros puntos
    Luego calculas el area del poligono formado por los puntos de interseccion con convex hull, por ejemplo.
4. Implement Delaunay triangulation without using Voronoi diagram
    Section 9.3 Computational Geometry
5. Implement Voronoi diagram without using Delaunay triangulation
    Fortune's algorithm

https://en.wikipedia.org/wiki/Delaunay_triangulation
Bowyer-Watson algorithm
    6. Implement Delaunay triangulation using Voronoi diagram
    7. Implement Voronoi diagram using Delaunay triangulation


https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.voronoi_plot_2d.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.delaunay_plot_2d.html
"""