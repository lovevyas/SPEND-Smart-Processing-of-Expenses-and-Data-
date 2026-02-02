import cv2
from PIL import Image

def preprocess_image(image_path: str) -> Image.Image:
    """
    Preprocessing for synthetic / digital receipts:
    - Upscale image
    - Preserve original sharpness
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found")

    # Upscale image (VERY IMPORTANT)
    scale_factor = 2
    resized = cv2.resize(
        image,
        None,
        fx=scale_factor,
        fy=scale_factor,
        interpolation=cv2.INTER_CUBIC
    )

    return Image.fromarray(resized)
