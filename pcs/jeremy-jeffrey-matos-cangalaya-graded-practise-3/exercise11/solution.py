import numpy as np
import matplotlib.pyplot as plt
import json
import math

"""
https://paulbourke.net/geometry/polygonise/
https://www.youtube.com/watch?v=5g7sL1RUu1I
Step 2:
    Classifiy each voxel according to whether it lies:
        - Outside the surface: value > isosurface value
        - Inside the surface: value <= isosurface value
Step 3:
    Use the binary labelling of each voxel vertex to create an index
Step 4:
    For a given index, access an array storing a list of edges
    All 256 cases can be derived from 1 + 14 = 15 base cases due to symmetries

    Get a edge list from lookup (case) table
        Decompose the case as a set of triangles
Step 5: 
    For each triangle edge, find the vertex location along the edge using the linear interpolation of the voxel values
Step 6:
    Calculate the normal at each cube vertex (central differences)
    Use linear interpolation to compute the polygon vertex normal (off the isosurface)
Step 7:
    Consider ambiguous cases
        - Ambiguous cases: 3, 6, 7, 10, 12, 13
        - Adjacent vertices: different states
        - Diagaonal vertices: same state
        - Resolution: choose one case (the right one)
"""


CASES = [
  [],
  [[8, 0, 3]],
  [[1, 0, 9]],
  [
    [8, 1, 3],
    [8, 9, 1]
  ],
  [[10, 2, 1]],
  [
    [8, 0, 3],
    [1, 10, 2]
  ],
  [
    [9, 2, 0],
    [9, 10, 2]
  ],
  [
    [3, 8, 2],
    [2, 8, 10],
    [10, 8, 9]
  ],
  [[3, 2, 11]],
  [
    [0, 2, 8],
    [2, 11, 8]
  ],
  [
    [1, 0, 9],
    [2, 11, 3]
  ],
  [
    [2, 9, 1],
    [11, 9, 2],
    [8, 9, 11]
  ],
  [
    [3, 10, 11],
    [3, 1, 10]
  ],
  [
    [1, 10, 0],
    [0, 10, 8],
    [8, 10, 11]
  ],
  [
    [0, 11, 3],
    [9, 11, 0],
    [10, 11, 9]
  ],
  [
    [8, 9, 11],
    [11, 9, 10]
  ],
  [[7, 4, 8]],
  [
    [3, 7, 0],
    [7, 4, 0]
  ],
  [
    [7, 4, 8],
    [9, 1, 0]
  ],
  [
    [9, 1, 4],
    [4, 1, 7],
    [7, 1, 3]
  ],
  [
    [7, 4, 8],
    [2, 1, 10]
  ],
  [
    [4, 3, 7],
    [4, 0, 3],
    [2, 1, 10]
  ],
  [
    [2, 0, 10],
    [0, 9, 10],
    [7, 4, 8]
  ],
  [
    [9, 10, 4],
    [4, 10, 3],
    [3, 10, 2],
    [4, 3, 7]
  ],
  [
    [4, 8, 7],
    [3, 2, 11]
  ],
  [
    [7, 4, 11],
    [11, 4, 2],
    [2, 4, 0]
  ],
  [
    [1, 0, 9],
    [2, 11, 3],
    [8, 7, 4]
  ],
  [
    [2, 11, 1],
    [1, 11, 9],
    [9, 11, 7],
    [9, 7, 4]
  ],
  [
    [10, 11, 1],
    [11, 3, 1],
    [4, 8, 7]
  ],
  [
    [4, 0, 7],
    [7, 0, 10],
    [0, 1, 10],
    [7, 10, 11]
  ],
  [
    [7, 4, 8],
    [0, 11, 3],
    [9, 11, 0],
    [10, 11, 9]
  ],
  [
    [4, 11, 7],
    [9, 11, 4],
    [10, 11, 9]
  ],
  [[9, 4, 5]],
  [
    [9, 4, 5],
    [0, 3, 8]
  ],
  [
    [0, 5, 1],
    [0, 4, 5]
  ],
  [
    [4, 3, 8],
    [5, 3, 4],
    [1, 3, 5]
  ],
  [
    [5, 9, 4],
    [10, 2, 1]
  ],
  [
    [8, 0, 3],
    [1, 10, 2],
    [4, 5, 9]
  ],
  [
    [10, 4, 5],
    [2, 4, 10],
    [0, 4, 2]
  ],
  [
    [3, 10, 2],
    [8, 10, 3],
    [5, 10, 8],
    [4, 5, 8]
  ],
  [
    [9, 4, 5],
    [11, 3, 2]
  ],
  [
    [11, 0, 2],
    [11, 8, 0],
    [9, 4, 5]
  ],
  [
    [5, 1, 4],
    [1, 0, 4],
    [11, 3, 2]
  ],
  [
    [5, 1, 4],
    [4, 1, 11],
    [1, 2, 11],
    [4, 11, 8]
  ],
  [
    [3, 10, 11],
    [3, 1, 10],
    [5, 9, 4]
  ],
  [
    [9, 4, 5],
    [1, 10, 0],
    [0, 10, 8],
    [8, 10, 11]
  ],
  [
    [5, 0, 4],
    [11, 0, 5],
    [11, 3, 0],
    [10, 11, 5]
  ],
  [
    [5, 10, 4],
    [4, 10, 8],
    [8, 10, 11]
  ],
  [
    [9, 7, 5],
    [9, 8, 7]
  ],
  [
    [0, 5, 9],
    [3, 5, 0],
    [7, 5, 3]
  ],
  [
    [8, 7, 0],
    [0, 7, 1],
    [1, 7, 5]
  ],
  [
    [7, 5, 3],
    [3, 5, 1]
  ],
  [
    [7, 5, 8],
    [5, 9, 8],
    [2, 1, 10]
  ],
  [
    [10, 2, 1],
    [0, 5, 9],
    [3, 5, 0],
    [7, 5, 3]
  ],
  [
    [8, 2, 0],
    [5, 2, 8],
    [10, 2, 5],
    [7, 5, 8]
  ],
  [
    [2, 3, 10],
    [10, 3, 5],
    [5, 3, 7]
  ],
  [
    [9, 7, 5],
    [9, 8, 7],
    [11, 3, 2]
  ],
  [
    [0, 2, 9],
    [9, 2, 7],
    [7, 2, 11],
    [9, 7, 5]
  ],
  [
    [3, 2, 11],
    [8, 7, 0],
    [0, 7, 1],
    [1, 7, 5]
  ],
  [
    [11, 1, 2],
    [7, 1, 11],
    [5, 1, 7]
  ],
  [
    [3, 1, 11],
    [11, 1, 10],
    [8, 7, 9],
    [9, 7, 5]
  ],
  [
    [11, 7, 0],
    [7, 5, 0],
    [5, 9, 0],
    [10, 11, 0],
    [1, 10, 0]
  ],
  [
    [0, 5, 10],
    [0, 7, 5],
    [0, 8, 7],
    [0, 10, 11],
    [0, 11, 3]
  ],
  [
    [10, 11, 5],
    [11, 7, 5]
  ],
  [[5, 6, 10]],
  [
    [8, 0, 3],
    [10, 5, 6]
  ],
  [
    [0, 9, 1],
    [5, 6, 10]
  ],
  [
    [8, 1, 3],
    [8, 9, 1],
    [10, 5, 6]
  ],
  [
    [1, 6, 2],
    [1, 5, 6]
  ],
  [
    [6, 2, 5],
    [2, 1, 5],
    [8, 0, 3]
  ],
  [
    [5, 6, 9],
    [9, 6, 0],
    [0, 6, 2]
  ],
  [
    [5, 8, 9],
    [2, 8, 5],
    [3, 8, 2],
    [6, 2, 5]
  ],
  [
    [3, 2, 11],
    [10, 5, 6]
  ],
  [
    [0, 2, 8],
    [2, 11, 8],
    [5, 6, 10]
  ],
  [
    [3, 2, 11],
    [0, 9, 1],
    [10, 5, 6]
  ],
  [
    [5, 6, 10],
    [2, 9, 1],
    [11, 9, 2],
    [8, 9, 11]
  ],
  [
    [11, 3, 6],
    [6, 3, 5],
    [5, 3, 1]
  ],
  [
    [11, 8, 6],
    [6, 8, 1],
    [1, 8, 0],
    [6, 1, 5]
  ],
  [
    [5, 0, 9],
    [6, 0, 5],
    [3, 0, 6],
    [11, 3, 6]
  ],
  [
    [6, 9, 5],
    [11, 9, 6],
    [8, 9, 11]
  ],
  [
    [7, 4, 8],
    [6, 10, 5]
  ],
  [
    [3, 7, 0],
    [7, 4, 0],
    [10, 5, 6]
  ],
  [
    [7, 4, 8],
    [6, 10, 5],
    [9, 1, 0]
  ],
  [
    [5, 6, 10],
    [9, 1, 4],
    [4, 1, 7],
    [7, 1, 3]
  ],
  [
    [1, 6, 2],
    [1, 5, 6],
    [7, 4, 8]
  ],
  [
    [6, 1, 5],
    [2, 1, 6],
    [0, 7, 4],
    [3, 7, 0]
  ],
  [
    [4, 8, 7],
    [5, 6, 9],
    [9, 6, 0],
    [0, 6, 2]
  ],
  [
    [2, 3, 9],
    [3, 7, 9],
    [7, 4, 9],
    [6, 2, 9],
    [5, 6, 9]
  ],
  [
    [2, 11, 3],
    [7, 4, 8],
    [10, 5, 6]
  ],
  [
    [6, 10, 5],
    [7, 4, 11],
    [11, 4, 2],
    [2, 4, 0]
  ],
  [
    [1, 0, 9],
    [8, 7, 4],
    [3, 2, 11],
    [5, 6, 10]
  ],
  [
    [1, 2, 9],
    [9, 2, 11],
    [9, 11, 4],
    [4, 11, 7],
    [5, 6, 10]
  ],
  [
    [7, 4, 8],
    [11, 3, 6],
    [6, 3, 5],
    [5, 3, 1]
  ],
  [
    [11, 0, 1],
    [11, 4, 0],
    [11, 7, 4],
    [11, 1, 5],
    [11, 5, 6]
  ],
  [
    [6, 9, 5],
    [0, 9, 6],
    [11, 0, 6],
    [3, 0, 11],
    [4, 8, 7]
  ],
  [
    [5, 6, 9],
    [9, 6, 11],
    [9, 11, 7],
    [9, 7, 4]
  ],
  [
    [4, 10, 9],
    [4, 6, 10]
  ],
  [
    [10, 4, 6],
    [10, 9, 4],
    [8, 0, 3]
  ],
  [
    [1, 0, 10],
    [10, 0, 6],
    [6, 0, 4]
  ],
  [
    [8, 1, 3],
    [6, 1, 8],
    [6, 10, 1],
    [4, 6, 8]
  ],
  [
    [9, 2, 1],
    [4, 2, 9],
    [6, 2, 4]
  ],
  [
    [3, 8, 0],
    [9, 2, 1],
    [4, 2, 9],
    [6, 2, 4]
  ],
  [
    [0, 4, 2],
    [2, 4, 6]
  ],
  [
    [8, 2, 3],
    [4, 2, 8],
    [6, 2, 4]
  ],
  [
    [4, 10, 9],
    [4, 6, 10],
    [2, 11, 3]
  ],
  [
    [11, 8, 2],
    [2, 8, 0],
    [6, 10, 4],
    [4, 10, 9]
  ],
  [
    [2, 11, 3],
    [1, 0, 10],
    [10, 0, 6],
    [6, 0, 4]
  ],
  [
    [8, 4, 1],
    [4, 6, 1],
    [6, 10, 1],
    [11, 8, 1],
    [2, 11, 1]
  ],
  [
    [3, 1, 11],
    [11, 1, 4],
    [1, 9, 4],
    [11, 4, 6]
  ],
  [
    [6, 11, 1],
    [11, 8, 1],
    [8, 0, 1],
    [4, 6, 1],
    [9, 4, 1]
  ],
  [
    [3, 0, 11],
    [11, 0, 6],
    [6, 0, 4]
  ],
  [
    [4, 11, 8],
    [4, 6, 11]
  ],
  [
    [6, 8, 7],
    [10, 8, 6],
    [9, 8, 10]
  ],
  [
    [3, 7, 0],
    [0, 7, 10],
    [7, 6, 10],
    [0, 10, 9]
  ],
  [
    [1, 6, 10],
    [0, 6, 1],
    [7, 6, 0],
    [8, 7, 0]
  ],
  [
    [10, 1, 6],
    [6, 1, 7],
    [7, 1, 3]
  ],
  [
    [9, 8, 1],
    [1, 8, 6],
    [6, 8, 7],
    [1, 6, 2]
  ],
  [
    [9, 7, 6],
    [9, 3, 7],
    [9, 0, 3],
    [9, 6, 2],
    [9, 2, 1]
  ],
  [
    [7, 6, 8],
    [8, 6, 0],
    [0, 6, 2]
  ],
  [
    [3, 6, 2],
    [3, 7, 6]
  ],
  [
    [3, 2, 11],
    [6, 8, 7],
    [10, 8, 6],
    [9, 8, 10]
  ],
  [
    [7, 9, 0],
    [7, 10, 9],
    [7, 6, 10],
    [7, 0, 2],
    [7, 2, 11]
  ],
  [
    [0, 10, 1],
    [6, 10, 0],
    [8, 6, 0],
    [7, 6, 8],
    [2, 11, 3]
  ],
  [
    [1, 6, 10],
    [7, 6, 1],
    [11, 7, 1],
    [2, 11, 1]
  ],
  [
    [1, 9, 6],
    [9, 8, 6],
    [8, 7, 6],
    [3, 1, 6],
    [11, 3, 6]
  ],
  [
    [9, 0, 1],
    [11, 7, 6]
  ],
  [
    [0, 11, 3],
    [6, 11, 0],
    [7, 6, 0],
    [8, 7, 0]
  ],
  [[7, 6, 11]],
  [[11, 6, 7]],
  [
    [3, 8, 0],
    [11, 6, 7]
  ],
  [
    [1, 0, 9],
    [6, 7, 11]
  ],
  [
    [1, 3, 9],
    [3, 8, 9],
    [6, 7, 11]
  ],
  [
    [10, 2, 1],
    [6, 7, 11]
  ],
  [
    [10, 2, 1],
    [3, 8, 0],
    [6, 7, 11]
  ],
  [
    [9, 2, 0],
    [9, 10, 2],
    [11, 6, 7]
  ],
  [
    [11, 6, 7],
    [3, 8, 2],
    [2, 8, 10],
    [10, 8, 9]
  ],
  [
    [2, 6, 3],
    [6, 7, 3]
  ],
  [
    [8, 6, 7],
    [0, 6, 8],
    [2, 6, 0]
  ],
  [
    [7, 2, 6],
    [7, 3, 2],
    [1, 0, 9]
  ],
  [
    [8, 9, 7],
    [7, 9, 2],
    [2, 9, 1],
    [7, 2, 6]
  ],
  [
    [6, 1, 10],
    [7, 1, 6],
    [3, 1, 7]
  ],
  [
    [8, 0, 7],
    [7, 0, 6],
    [6, 0, 1],
    [6, 1, 10]
  ],
  [
    [7, 3, 6],
    [6, 3, 9],
    [3, 0, 9],
    [6, 9, 10]
  ],
  [
    [7, 8, 6],
    [6, 8, 10],
    [10, 8, 9]
  ],
  [
    [8, 11, 4],
    [11, 6, 4]
  ],
  [
    [11, 0, 3],
    [6, 0, 11],
    [4, 0, 6]
  ],
  [
    [6, 4, 11],
    [4, 8, 11],
    [1, 0, 9]
  ],
  [
    [1, 3, 9],
    [9, 3, 6],
    [3, 11, 6],
    [9, 6, 4]
  ],
  [
    [8, 11, 4],
    [11, 6, 4],
    [1, 10, 2]
  ],
  [
    [1, 10, 2],
    [11, 0, 3],
    [6, 0, 11],
    [4, 0, 6]
  ],
  [
    [2, 9, 10],
    [0, 9, 2],
    [4, 11, 6],
    [8, 11, 4]
  ],
  [
    [3, 4, 9],
    [3, 6, 4],
    [3, 11, 6],
    [3, 9, 10],
    [3, 10, 2]
  ],
  [
    [3, 2, 8],
    [8, 2, 4],
    [4, 2, 6]
  ],
  [
    [2, 4, 0],
    [6, 4, 2]
  ],
  [
    [0, 9, 1],
    [3, 2, 8],
    [8, 2, 4],
    [4, 2, 6]
  ],
  [
    [1, 2, 9],
    [9, 2, 4],
    [4, 2, 6]
  ],
  [
    [10, 3, 1],
    [4, 3, 10],
    [4, 8, 3],
    [6, 4, 10]
  ],
  [
    [10, 0, 1],
    [6, 0, 10],
    [4, 0, 6]
  ],
  [
    [3, 10, 6],
    [3, 9, 10],
    [3, 0, 9],
    [3, 6, 4],
    [3, 4, 8]
  ],
  [
    [9, 10, 4],
    [10, 6, 4]
  ],
  [
    [9, 4, 5],
    [7, 11, 6]
  ],
  [
    [9, 4, 5],
    [7, 11, 6],
    [0, 3, 8]
  ],
  [
    [0, 5, 1],
    [0, 4, 5],
    [6, 7, 11]
  ],
  [
    [11, 6, 7],
    [4, 3, 8],
    [5, 3, 4],
    [1, 3, 5]
  ],
  [
    [1, 10, 2],
    [9, 4, 5],
    [6, 7, 11]
  ],
  [
    [8, 0, 3],
    [4, 5, 9],
    [10, 2, 1],
    [11, 6, 7]
  ],
  [
    [7, 11, 6],
    [10, 4, 5],
    [2, 4, 10],
    [0, 4, 2]
  ],
  [
    [8, 2, 3],
    [10, 2, 8],
    [4, 10, 8],
    [5, 10, 4],
    [11, 6, 7]
  ],
  [
    [2, 6, 3],
    [6, 7, 3],
    [9, 4, 5]
  ],
  [
    [5, 9, 4],
    [8, 6, 7],
    [0, 6, 8],
    [2, 6, 0]
  ],
  [
    [7, 3, 6],
    [6, 3, 2],
    [4, 5, 0],
    [0, 5, 1]
  ],
  [
    [8, 1, 2],
    [8, 5, 1],
    [8, 4, 5],
    [8, 2, 6],
    [8, 6, 7]
  ],
  [
    [9, 4, 5],
    [6, 1, 10],
    [7, 1, 6],
    [3, 1, 7]
  ],
  [
    [7, 8, 6],
    [6, 8, 0],
    [6, 0, 10],
    [10, 0, 1],
    [5, 9, 4]
  ],
  [
    [3, 0, 10],
    [0, 4, 10],
    [4, 5, 10],
    [7, 3, 10],
    [6, 7, 10]
  ],
  [
    [8, 6, 7],
    [10, 6, 8],
    [5, 10, 8],
    [4, 5, 8]
  ],
  [
    [5, 9, 6],
    [6, 9, 11],
    [11, 9, 8]
  ],
  [
    [11, 6, 3],
    [3, 6, 0],
    [0, 6, 5],
    [0, 5, 9]
  ],
  [
    [8, 11, 0],
    [0, 11, 5],
    [5, 11, 6],
    [0, 5, 1]
  ],
  [
    [6, 3, 11],
    [5, 3, 6],
    [1, 3, 5]
  ],
  [
    [10, 2, 1],
    [5, 9, 6],
    [6, 9, 11],
    [11, 9, 8]
  ],
  [
    [3, 11, 0],
    [0, 11, 6],
    [0, 6, 9],
    [9, 6, 5],
    [1, 10, 2]
  ],
  [
    [0, 8, 5],
    [8, 11, 5],
    [11, 6, 5],
    [2, 0, 5],
    [10, 2, 5]
  ],
  [
    [11, 6, 3],
    [3, 6, 5],
    [3, 5, 10],
    [3, 10, 2]
  ],
  [
    [3, 9, 8],
    [6, 9, 3],
    [5, 9, 6],
    [2, 6, 3]
  ],
  [
    [9, 6, 5],
    [0, 6, 9],
    [2, 6, 0]
  ],
  [
    [6, 5, 8],
    [5, 1, 8],
    [1, 0, 8],
    [2, 6, 8],
    [3, 2, 8]
  ],
  [
    [2, 6, 1],
    [6, 5, 1]
  ],
  [
    [6, 8, 3],
    [6, 9, 8],
    [6, 5, 9],
    [6, 3, 1],
    [6, 1, 10]
  ],
  [
    [1, 10, 0],
    [0, 10, 6],
    [0, 6, 5],
    [0, 5, 9]
  ],
  [
    [3, 0, 8],
    [6, 5, 10]
  ],
  [[10, 6, 5]],
  [
    [5, 11, 10],
    [5, 7, 11]
  ],
  [
    [5, 11, 10],
    [5, 7, 11],
    [3, 8, 0]
  ],
  [
    [11, 10, 7],
    [10, 5, 7],
    [0, 9, 1]
  ],
  [
    [5, 7, 10],
    [10, 7, 11],
    [9, 1, 8],
    [8, 1, 3]
  ],
  [
    [2, 1, 11],
    [11, 1, 7],
    [7, 1, 5]
  ],
  [
    [3, 8, 0],
    [2, 1, 11],
    [11, 1, 7],
    [7, 1, 5]
  ],
  [
    [2, 0, 11],
    [11, 0, 5],
    [5, 0, 9],
    [11, 5, 7]
  ],
  [
    [2, 9, 5],
    [2, 8, 9],
    [2, 3, 8],
    [2, 5, 7],
    [2, 7, 11]
  ],
  [
    [10, 3, 2],
    [5, 3, 10],
    [7, 3, 5]
  ],
  [
    [10, 0, 2],
    [7, 0, 10],
    [8, 0, 7],
    [5, 7, 10]
  ],
  [
    [0, 9, 1],
    [10, 3, 2],
    [5, 3, 10],
    [7, 3, 5]
  ],
  [
    [7, 8, 2],
    [8, 9, 2],
    [9, 1, 2],
    [5, 7, 2],
    [10, 5, 2]
  ],
  [
    [3, 1, 7],
    [7, 1, 5]
  ],
  [
    [0, 7, 8],
    [1, 7, 0],
    [5, 7, 1]
  ],
  [
    [9, 5, 0],
    [0, 5, 3],
    [3, 5, 7]
  ],
  [
    [5, 7, 9],
    [7, 8, 9]
  ],
  [
    [4, 10, 5],
    [8, 10, 4],
    [11, 10, 8]
  ],
  [
    [3, 4, 0],
    [10, 4, 3],
    [10, 5, 4],
    [11, 10, 3]
  ],
  [
    [1, 0, 9],
    [4, 10, 5],
    [8, 10, 4],
    [11, 10, 8]
  ],
  [
    [4, 3, 11],
    [4, 1, 3],
    [4, 9, 1],
    [4, 11, 10],
    [4, 10, 5]
  ],
  [
    [1, 5, 2],
    [2, 5, 8],
    [5, 4, 8],
    [2, 8, 11]
  ],
  [
    [5, 4, 11],
    [4, 0, 11],
    [0, 3, 11],
    [1, 5, 11],
    [2, 1, 11]
  ],
  [
    [5, 11, 2],
    [5, 8, 11],
    [5, 4, 8],
    [5, 2, 0],
    [5, 0, 9]
  ],
  [
    [5, 4, 9],
    [2, 3, 11]
  ],
  [
    [3, 4, 8],
    [2, 4, 3],
    [5, 4, 2],
    [10, 5, 2]
  ],
  [
    [5, 4, 10],
    [10, 4, 2],
    [2, 4, 0]
  ],
  [
    [2, 8, 3],
    [4, 8, 2],
    [10, 4, 2],
    [5, 4, 10],
    [0, 9, 1]
  ],
  [
    [4, 10, 5],
    [2, 10, 4],
    [1, 2, 4],
    [9, 1, 4]
  ],
  [
    [8, 3, 4],
    [4, 3, 5],
    [5, 3, 1]
  ],
  [
    [1, 5, 0],
    [5, 4, 0]
  ],
  [
    [5, 0, 9],
    [3, 0, 5],
    [8, 3, 5],
    [4, 8, 5]
  ],
  [[5, 4, 9]],
  [
    [7, 11, 4],
    [4, 11, 9],
    [9, 11, 10]
  ],
  [
    [8, 0, 3],
    [7, 11, 4],
    [4, 11, 9],
    [9, 11, 10]
  ],
  [
    [0, 4, 1],
    [1, 4, 11],
    [4, 7, 11],
    [1, 11, 10]
  ],
  [
    [10, 1, 4],
    [1, 3, 4],
    [3, 8, 4],
    [11, 10, 4],
    [7, 11, 4]
  ],
  [
    [9, 4, 1],
    [1, 4, 2],
    [2, 4, 7],
    [2, 7, 11]
  ],
  [
    [1, 9, 2],
    [2, 9, 4],
    [2, 4, 11],
    [11, 4, 7],
    [3, 8, 0]
  ],
  [
    [11, 4, 7],
    [2, 4, 11],
    [0, 4, 2]
  ],
  [
    [7, 11, 4],
    [4, 11, 2],
    [4, 2, 3],
    [4, 3, 8]
  ],
  [
    [10, 9, 2],
    [2, 9, 7],
    [7, 9, 4],
    [2, 7, 3]
  ],
  [
    [2, 10, 7],
    [10, 9, 7],
    [9, 4, 7],
    [0, 2, 7],
    [8, 0, 7]
  ],
  [
    [10, 4, 7],
    [10, 0, 4],
    [10, 1, 0],
    [10, 7, 3],
    [10, 3, 2]
  ],
  [
    [8, 4, 7],
    [10, 1, 2]
  ],
  [
    [4, 1, 9],
    [7, 1, 4],
    [3, 1, 7]
  ],
  [
    [8, 0, 7],
    [7, 0, 1],
    [7, 1, 9],
    [7, 9, 4]
  ],
  [
    [0, 7, 3],
    [0, 4, 7]
  ],
  [[8, 4, 7]],
  [
    [9, 8, 10],
    [10, 8, 11]
  ],
  [
    [3, 11, 0],
    [0, 11, 9],
    [9, 11, 10]
  ],
  [
    [0, 10, 1],
    [8, 10, 0],
    [11, 10, 8]
  ],
  [
    [11, 10, 3],
    [10, 1, 3]
  ],
  [
    [1, 9, 2],
    [2, 9, 11],
    [11, 9, 8]
  ],
  [
    [9, 2, 1],
    [11, 2, 9],
    [3, 11, 9],
    [0, 3, 9]
  ],
  [
    [8, 2, 0],
    [8, 11, 2]
  ],
  [[11, 2, 3]],
  [
    [2, 8, 3],
    [10, 8, 2],
    [9, 8, 10]
  ],
  [
    [0, 2, 9],
    [2, 10, 9]
  ],
  [
    [3, 2, 8],
    [8, 2, 10],
    [8, 10, 1],
    [8, 1, 0]
  ],
  [[1, 2, 10]],
  [
    [3, 1, 8],
    [1, 9, 8]
  ],
  [[9, 0, 1]],
  [[3, 0, 8]],
  []
]


N_SAMPLING = 10000

class Mesh:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.index: int = 0

    def add_triangle(self, pol) -> None:
        for v in pol:
            t: tuple[float, float, float] = (v[0], v[1], v[2])
            self.vertices.append(t)

        self.index += 3
        self.faces.append([self.index - 3, self.index - 1, self.index - 2])

    def create_off(self, output_file: str) -> None:
        file = open(output_file, mode="w")
        file.write("OFF\n")
        file.write(f"{len(self.vertices)} {len(self.faces)} {len(self.vertices)}\n\n")

        for v in self.vertices:
            for p in v:
                file.write(f"{p} ")
            file.write("\n")
        file.write("\n")

        for face in self.faces:
            file.write(f"{len(face)} ")
            for i in face:
                file.write(f"{i} ")
            file.write("\n")
        file.close()


GLOBAL_MESH = Mesh()


def dist(p1: np.ndarray, p2: np.ndarray) -> float:
    return math.sqrt(
        pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2)
    )


def generate_random_points(
    n: int, x_range: tuple, y_range: tuple, z_range: tuple
) -> np.ndarray:
    x_points = np.random.uniform(x_range[0], x_range[1], n)
    y_points = np.random.uniform(y_range[0], y_range[1], n)
    z_points = np.random.uniform(z_range[0], z_range[1], n)

    return np.column_stack((x_points, y_points, z_points))


def divide_cube(cube_box: tuple) -> list:
    min_point, max_point = cube_box
    mid_point = (min_point + max_point) / 2

    new_cubes = [
        (min_point, mid_point),
        (
            np.array([mid_point[0], min_point[1], min_point[2]]),
            np.array([max_point[0], mid_point[1], mid_point[2]]),
        ),
        (
            np.array([min_point[0], mid_point[1], min_point[2]]),
            np.array([mid_point[0], max_point[1], mid_point[2]]),
        ),
        (
            np.array([mid_point[0], mid_point[1], min_point[2]]),
            np.array([max_point[0], max_point[1], mid_point[2]]),
        ),
        (
            np.array([min_point[0], min_point[1], mid_point[2]]),
            np.array([mid_point[0], mid_point[1], max_point[2]]),
        ),
        (
            np.array([mid_point[0], min_point[1], mid_point[2]]),
            np.array([max_point[0], mid_point[1], max_point[2]]),
        ),
        (
            np.array([min_point[0], mid_point[1], mid_point[2]]),
            np.array([mid_point[0], max_point[1], max_point[2]]),
        ),
        (mid_point, max_point),
    ]
    return new_cubes


def get_vertexes_from_cube_box(cube_box: tuple) -> np.ndarray:
    min_point, max_point = cube_box
    x_min, y_min, z_min = min_point
    x_max, y_max, z_max = max_point

    return np.array(
        [
            [x_min, y_min, z_min],
            [x_max, y_min, z_min],
            [x_max, y_max, z_min],
            [x_min, y_max, z_min],
            [x_min, y_min, z_max],
            [x_max, y_min, z_max],
            [x_max, y_max, z_max],
            [x_min, y_max, z_max],
        ]
    )


def get_edges_from_cube_box(cube_box: tuple) -> list:
    edge_idx = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]
    vertexes = get_vertexes_from_cube_box(cube_box)
    return [(vertexes[i], vertexes[j]) for i, j in edge_idx]


def add_surface(f, cube_box):
    global GLOBAL_MESH, CASES
    vertexes = get_vertexes_from_cube_box(cube_box)

    result = f(vertexes[:, 0], vertexes[:, 1], vertexes[:, 2])
    case = 0
    for i, val in enumerate(result):
        if val > 0:
            case += pow(2, i)

    edges = get_edges_from_cube_box(cube_box)
    fig_case = CASES[case]

    for edge_idx in fig_case:
        ed_1, ed_2, ed_3 = edges[edge_idx[0]], edges[edge_idx[1]], edges[edge_idx[2]]
        v_1 = (ed_1[0] + ed_1[1]) / 2
        v_2 = (ed_2[0] + ed_2[1]) / 2
        v_3 = (ed_3[0] + ed_3[1]) / 2

        GLOBAL_MESH.add_triangle([v_1, v_2, v_3])


def marching_cubes_compute(f, cube_box: tuple, precision: float = 0.025, n_sampling = N_SAMPLING, depth: int = 0):
    if depth == 0:
        global GLOBAL_MESH
        GLOBAL_MESH = Mesh()

    min_point, max_point = cube_box
    x_min, y_min, z_min = min_point
    x_max, y_max, z_max = max_point

    p_sampling = np.vstack(
        [
            generate_random_points(
                n_sampling, (x_min, x_max), (y_min, y_max), (z_min, z_max)
            ),
            get_vertexes_from_cube_box(cube_box),
        ]
    )
    eval_points = f(p_sampling[:, 0], p_sampling[:, 1], p_sampling[:, 2])
    
    # * contar (+) (-) (0)
    n_positives = len(eval_points[eval_points > 0])  # outside: todos -> afuera
    n_negatives = len(eval_points[eval_points < 0])  # inside: todos -> adentro
    n_zeros = len(eval_points[eval_points == 0])  # border
    
    if n_zeros == 0:
        if n_negatives > 0 and n_positives == 0:
            # cubo esta totalmente adentro
            return
        if n_positives > 0 and n_negatives == 0:
            # cubo esta totalmente afuera
            return

    if (
        x_max - x_min < precision
        and y_max - y_min < precision
        and z_max - z_min < precision
    ):
        add_surface(f, cube_box)
        return

    for each_cube in divide_cube(cube_box):
        # min(n_sampling // 8, 100)
        marching_cubes_compute(f, each_cube, precision, n_sampling, depth + 1)


def eval_obj(json_obj: dict, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    if json_obj["op"] == "union":
        # result_childs = np.array([eval_obj(child, x, y) for child in json_obj['childs']])

        result_childs = []
        for child in json_obj["childs"]:
            result_childs.append(eval_obj(child, x, y, z))

        n_neg = np.sum(np.array(result_childs) < 0, axis=0)
        n_zeros = np.sum(np.array(result_childs) == 0, axis=0)
        result = np.where(n_neg > 0, -1, np.where(n_zeros > 0, 0, 1))

        return result
    elif json_obj['op'] == 'intersection':
        first_child_result = eval_obj(json_obj['childs'][0], x, y, z)
        other_children_results = np.array([eval_obj(child, x, y, z) for child in json_obj['childs'][1:]])
        result = np.where(first_child_result < 0, np.min(other_children_results, axis=0), 1)
        result = np.where(result >= 0, 1, -1)  # Difference: inside if in first but not in others
        return result

    elif json_obj['op'] == 'difference':
        first_child_result = eval_obj(json_obj['childs'][0], x, y, z)
        other_children_results = [eval_obj(child, x, y, z) for child in json_obj['childs'][1:]]

        other_children_union = np.full_like(first_child_result, 1)
        for result in other_children_results:
            other_children_union = np.minimum(other_children_union, result)
        
        result = np.where(first_child_result < 0, 
                          np.where(other_children_union < 0, 1, -1), 
                          np.where(other_children_union < 0, 1, 1))

        return result


    elif json_obj["op"] == "":
        return json_obj["function"](x=x, y=y, z=z)


def transform_functions_to_lambdas(node: dict):
    if "function" in node and node["function"]:
        node["function"] = eval(f"lambda x, y, z: {node['function'].replace('^', '**')}")
    if "childs" in node and node["childs"]:
        for child in node["childs"]:
            transform_functions_to_lambdas(child)


def marching_cubes(
    json_object_describing_surface: dict,
    output_filename: str,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
    z_min: float,
    z_max: float,
    precision: float,
):
    transform_functions_to_lambdas(json_object_describing_surface)
    def json_func(x, y, z) -> int:
        return eval_obj(json_object_describing_surface, x, y, z)

    marching_cubes_compute(
        json_func,
        (np.array([x_min, y_min, z_min]), np.array([x_max, y_max, z_max])),
        precision,
    )

    GLOBAL_MESH.create_off(output_filename)


if __name__ == "__main__":
    marching_cubes(
        # sphere of radius 1 centered at (2, 2, 2)
        {"op": "", "function": "(x-2)^2+(y-2)^2+(z-2)^2-1", "childs": []},
        "./example-marching-cubes_2.off",
        -5, -5, 10, 10, -5, 10, 0.1
    )

    marching_cubes(
        {
            "op": "difference",
            "function": "",
            "childs": [
                {"op": "", "function": "(x-2)^2+(y-2)^2+(z-2)^2-1", "childs": []},
                {"op": "", "function": "(x-3)^2+(y-2)^2+(z-2)^2-1", "childs": []},
            ],
        },
        "./example-marching-cubes_3.off",
        -5, -5, 10, 10, -5, 10, 0.1
    )
