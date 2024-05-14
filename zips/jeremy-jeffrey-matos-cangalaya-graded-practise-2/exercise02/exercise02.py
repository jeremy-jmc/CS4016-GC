"""
Write a function that receives a list of vertices of a polygon, given by its coordinates, and decides if the polygon convex or not.

IDEA: sort the vertices by the angle they form with the first vertex. Then, check if the polygon is convex by checking the sign of the cross product of the vectors formed by the sorted vertices.
"""
