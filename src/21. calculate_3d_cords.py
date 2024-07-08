def calculate_3d_coordinates(baseline, focal_length, pixel_size, xL, yL, xR, yR):
    print(f"Datos dados:\n"
          f" - Línea base (b): {baseline} mm\n"
          f" - Longitud focal (f): {focal_length} mm\n"
          f" - Tamaño del píxel: {pixel_size} mm\n"
          f" - Coordenadas del píxel en la imagen izquierda (xL, yL): ({xL}, {yL})\n"
          f" - Coordenadas del píxel en la imagen derecha (xR, yR): ({xR}, {yR})\n")

    # Paso 1: Calcular la disparidad
    d = xL - xR
    print(f"Paso 1: Calcular la disparidad\n"
          f" - Disparidad (d) = xL - xR = {xL} - {xR} = {d} píxeles\n")

    # Paso 2: Convertir la disparidad a milímetros
    d_mm = d * pixel_size
    print(f"Paso 2: Convertir la disparidad a milímetros\n"
          f" - Disparidad en mm (d_mm) = d * tamaño del píxel = {d} * {pixel_size} = {d_mm} mm\n")

    # Paso 3: Calcular Z
    Z = (baseline * focal_length) / d_mm
    print(f"Paso 3: Calcular Z\n"
          f" - Profundidad (Z) = (b * f) / d_mm = ({baseline} * {focal_length}) / {d_mm} = {Z} mm\n")

    # Paso 4: Calcular X
    X = (baseline * (xL + xR)) / (2 * d_mm)
    print(f"Paso 4: Calcular X\n"
          f" - Coordenada Horizontal (X) = (b * (xL + xR)) / (2 * d_mm) = ({baseline} * ({xL} + {xR})) / (2 * {d_mm}) = {X} mm\n")

    # Paso 5: Calcular Y
    y_mm = yL * pixel_size
    Y = (baseline * y_mm) / d_mm
    print(f"Paso 5: Calcular Y\n"
          f" - Coordenada Vertical (Y) = (b * y_mm) / d_mm = ({baseline} * {y_mm}) / {d_mm} = {Y} mm\n")

    # Convertir a metros para mayor claridad
    X_m = X / 1000
    Y_m = Y / 1000
    Z_m = Z / 1000

    print(f"Conclusión:\n"
          f"Las coordenadas 3D (X, Y, Z) del punto son: ({X_m} m, {Y_m} m, {Z_m} m)")

    return X_m, Y_m, Z_m


# Ejemplo de uso
baseline = 100  # mm
focal_length = 50  # mm
pixel_size = 0.01  # mm
xL = 150  # píxeles
yL = 200  # píxeles
xR = 130  # píxeles
yR = 200  # píxeles

calculate_3d_coordinates(baseline, focal_length, pixel_size, xL, yL, xR, yR)
