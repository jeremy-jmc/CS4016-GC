def highlight_people_cars_and_bikes(
    full_path_input_image,
    color_scale_image,
    color_scale_people,
    color_scale_cars,
    color_scale_bikes,
    full_path_output_image,
):
    pass


if __name__ == "__main__":
    highlight_people_cars_and_bikes(
        full_path_input_image="example-1.jpg",
        color_scale_image=(255, 255, 255),
        color_scale_people=(255, 0, 0),
        color_scale_cars=(0, 255, 0),
        color_scale_bikes=(0, 0, 255),
        full_path_output_image="detections-example-1.jpg",
    )
