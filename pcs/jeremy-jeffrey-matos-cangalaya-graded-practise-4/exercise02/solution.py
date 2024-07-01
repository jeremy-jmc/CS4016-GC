def sequence_of_projections(
    full_path_input_mesh,
    optical_center_x,
    optical_center_y,
    optical_center_z,
    optical_axis_x,
    optical_axis_y,
    optical_axis_z,
    output_width_in_pixels,
    output_height_in_pixels,
    prefix_output_files,
):
    pass


if __name__ == "__main__":
    sequence_of_projections(
        full_path_input_mesh="sphere-rectangles.off",
        optical_center_x=[4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0],
        optical_center_y=[5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        optical_center_z=[5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        optical_axis_x=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        optical_axis_y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        optical_axis_z=[-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
        output_width_in_pixels=1920,
        output_height_in_pixels=1080,
        prefix_output_files="cloud_of_points_moving_camera",
    )
