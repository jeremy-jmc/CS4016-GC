def calculate_barycentric_coordinates(P, A, B, C):
    # Puntos de los vértices del triángulo
    xA, yA = A
    xB, yB = B
    xC, yC = C

    # Coordeninadas del punto P
    x, y = P

    # Calculando las coordenadas baricéntricas
    denominator = (yB - yC) * (xA - xC) + (xC - xB) * (yA - yC)

    alpha = ((yB - yC) * (x - xC) + (xC - xB) * (y - yC)) / denominator
    beta = ((yC - yA) * (x - xC) + (xA - xC) * (y - yC)) / denominator
    gamma = 1.0 - alpha - beta

    print(
        f"1. Coordenadas baricéntricas para el punto P{P}: (alpha, beta, gamma) = ({alpha}, {beta}, {gamma})")

    return alpha, beta, gamma


def calculate_texture_coordinates(P, A, B, C, texA, texB, texC):
    alpha, beta, gamma = calculate_barycentric_coordinates(P, A, B, C)

    uA, vA = texA
    uB, vB = texB
    uC, vC = texC

    u = alpha * uA + beta * uB + gamma * uC
    v = alpha * vA + beta * vB + gamma * vC

    print(f"2. Coordenadas de textura para el punto P{P}: (u, v) = ({u}, {v})")

    return u, v


# Ejemplo numérico
P = (0.25, 0.25)
A = (0, 0)
B = (1, 0)
C = (0, 1)
texA = (0, 0)
texB = (1, 0)
texC = (0, 1)

print(f"Datos del triángulo y del punto P:")
print(f"Punto P: {P}")
print(f"Vértices del triángulo: A{A}, B{B}, C{C}")
print(f"Coordenadas de textura en los vértices: A{texA}, B{texB}, C{texC}")

u, v = calculate_texture_coordinates(P, A, B, C, texA, texB, texC)
