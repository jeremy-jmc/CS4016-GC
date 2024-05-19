"""
Write a function that computes the number of triangulations of a n-regular polygon. 
Explain your solution.

https://math.stackexchange.com/questions/1986709/triangulations-of-n-gon
https://math.stackexchange.com/questions/4324425/recursivley-count-triangulations-of-a-convex-polygon
TODO: explain de idea
"""

# -----------------------------------------------------------------------------
# Algorithm solution
# -----------------------------------------------------------------------------


def number_of_triangulations_nregular_polygon(n: int) -> int:
    T_n = [0] * (n + 1)
    T_n[0] = T_n[1] = 0
    T_n[2] = 1

    for i in range(3, n + 1):
        for k in range(2, i):
            # print(f'T_n[{i}] += T_n[{k}] * T_n[{i - k + 1}]')
            T_n[i] += T_n[k] * T_n[i - k + 1]
    # print(T_n)
    return T_n[n]

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test(n: int, expected: int):
    result = number_of_triangulations_nregular_polygon(n)
    if result == expected:
        print('Test passed')
    else:
        print(f'Test failed: expected {expected} but got {result}')


test(4, 2)
test(5, 5)
test(6, 14)
