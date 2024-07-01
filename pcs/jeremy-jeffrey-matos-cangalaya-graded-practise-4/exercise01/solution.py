def project_points(
    full_path_input_mesh,
    optical_center_x,
    optical_center_y,
    optical_center_z,
    optical_axis_x,
    optical_axis_y,
    optical_axis_z,
    output_width_in_pixels,
    output_height_in_pixels,
    full_path_output,
):
    pass


if __name__ == "__main__":
    project_points(
        full_path_input_mesh="sphere-rectangles.off",
        optical_center_x=5.0,
        optical_center_y=5.0,
        optical_center_z=5.0,
        optical_axis_x=0,
        optical_axis_y=0,
        optical_axis_z=-1.0,
        output_width_in_pixels=1920,
        output_height_in_pixels=1080,
        full_path_output="projection-1.png",
    )
