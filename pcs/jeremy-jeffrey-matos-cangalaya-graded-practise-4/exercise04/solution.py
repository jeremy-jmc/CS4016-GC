from cv2 import (
    AKAZE,
    ORB,
    SIFT,
    SURF,
    Affine,
    AffineBestOf2Nearest,
    BestOf2NearestRange,
    CompressedRectilinear,
    CompressedRectilinearPortrait,
    Cylindrical,
    FeatherBlender,
    Fisheye,
    Mercator,
    MultiBandBlender,
    Panini,
    PaniniPortrait,
    Plane,
    Spherical,
    Stereographic,
    TransverseMercator,
)

def stitch_images(
    full_path_input_image,
    blender,  # ={FeatherBlender | MultiBandBlender}
    features_finder,  # ={AKAZE | ORB | SIFT | SURF}
    features_matcher,  # ={AffineBestOf2Nearest | BestOf2NearestRange}
    warper,  # ={ Affine | CompressedRectilinearPortrait | CompressedRectilinear | Cylindrical | Fisheye | Mercator | PaniniPortrait | Panini | Plane | Spherical | Stereographic | TransverseMercator }
    full_path_output_image,
):
    pass


if __name__ == "__main__":
    stitch_images(
        full_path_input_image=[
            "panorama1-input-1.jpg",
            "panorama1-input-2.jpg",
            "panorama1-input-3.jpg",
            "panorama1-input-4.jpg",
            "panorama1-input-5.jpg",
            "panorama1-input-6.jpg",
        ],
        blender=MultiBandBlender,
        features_finder=SIFT,
        features_matcher=BestOf2NearestRange,
        warper=Mercator,
        full_path_output_image="panorama1-mercator.jpg",
    )

"""
    stitch_images(
        full_path_input_image="image-1.jpg",
        blender=FeatherBlender,
        features_finder=AKAZE,
        features_matcher=AffineBestOf2Nearest,
        warper=Affine,
        full_path_output_image="panorama-1.jpg",
    )
    stitch_images(
        full_path_input_image="image-2.jpg",
        blender=MultiBandBlender,
        features_finder=ORB,
        features_matcher=BestOf2NearestRange,
        warper=CompressedRectilinearPortrait,
        full_path_output_image="panorama-2.jpg",
    )
    stitch_images(
        full_path_input_image="image-3.jpg",
        blender=FeatherBlender,
        features_finder=SIFT,
        features_matcher=AffineBestOf2Nearest,
        warper=CompressedRectilinear,
        full_path_output_image="panorama-3.jpg",
    )
    stitch_images(
        full_path_input_image="image-4.jpg",
        blender=MultiBandBlender,
        features_finder=SURF,
        features_matcher=AffineBestOf2Nearest,
        warper=Cylindrical,
        full_path_output_image="panorama-4.jpg",
    )
    stitch_images(
        full_path_input_image="image-5.jpg",
        blender=FeatherBlender,
        features_finder=AKAZE,
        features_matcher=BestOf2NearestRange,
        warper=Fisheye,
        full_path_output_image="panorama-5.jpg",
    )
    stitch_images(
        full_path_input_image="image-6.jpg",
        blender=MultiBandBlender,
        features_finder=ORB,
        features_matcher=AffineBestOf2Nearest,
        warper=Mercator,
        full_path_output_image="panorama-6.jpg",
    )
    stitch_images(
        full_path_input_image="image-7.jpg",
        blender=FeatherBlender,
        features_finder=SIFT,
        features_matcher=BestOf2NearestRange,
        warper=PaniniPortrait,
        full_path_output_image="panorama-7.jpg",
    )
    stitch_images(
        full_path_input_image="image-8.jpg",
        blender=MultiBandBlender,
        features_finder=SURF,
        features_matcher=AffineBestOf2Nearest,
        warper=Panini,
    )
"""
