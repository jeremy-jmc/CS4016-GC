def calculate_focal_length(sensor_width, distance_to_object, object_percentage_on_sensor):
    """
    Calcula la longitud focal de una cámara estenopeica.

    Parameters:
    sensor_width (float): Ancho del sensor en mm.
    distance_to_object (float): Distancia al objeto en mm.
    object_percentage_on_sensor (float): Porcentaje del ancho del sensor que el objeto debe ocupar (entre 0 y 1).

    Returns:
    float: Longitud focal en mm.
    """
    object_width_on_sensor = object_percentage_on_sensor * sensor_width
    focal_length = (object_width_on_sensor * distance_to_object) / sensor_width
    return focal_length


# Parámetros
sensor_width = 35.0  # Ancho del sensor en mm
distance_to_object = 3000.0  # Distancia al objeto en mm (3 metros)
# Porcentaje del ancho del sensor que el objeto debe ocupar
object_percentage_on_sensor = 0.7

# Calcular longitud focal
focal_length = calculate_focal_length(
    sensor_width, distance_to_object, object_percentage_on_sensor)
print(
    f"La longitud focal de la cámara estenopeica debe ser de {focal_length:.2f} mm.")
