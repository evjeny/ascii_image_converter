import os
from typing import Optional

import numpy as np
from PIL import Image

from brightness_levels import get_symbols, read_sorted_mapping


def resize_image(
        image: Image.Image,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None
) -> Image.Image:
    width, height = image.size
    if target_width or target_height:
        if target_width:
            target_height = int(height * target_width / width)
        elif target_height:
            target_width = int(width * target_height / height)

        return image.resize((target_width, target_height))
    return image


def convert_brightness(
        image: Image.Image,
        sorted_brightness_config: Optional[list[tuple[float, str]]] = None,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None
) -> list[str]:
    if not sorted_brightness_config:
        sorted_brightness_config = read_sorted_mapping(
            os.path.join("precomputed_mappings", "mean.json")
        )

    grayscale_image = Image.new("L", image.size)
    grayscale_image.paste(image, (0, 0))

    grayscale_image = resize_image(grayscale_image, target_width, target_height)

    array = np.array(grayscale_image) / 255.0
    height, width = array.shape

    symbols = get_symbols(array.reshape(-1), sorted_brightness_config)

    return [symbols[i * width: (i + 1) * width] for i in range(height)]


def convert_brightness_rgb(
        image: Image.Image,
        sorted_brightness_config: Optional[list[tuple[float, str]]] = None,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None
) -> tuple[list[str], list[list[tuple[int, int, int]]]]:
    image = resize_image(image, target_width, target_height)
    image_ascii = convert_brightness(image, sorted_brightness_config)

    image_rgb = Image.new("RGB", image.size)
    image_rgb.paste(image)
    colors = np.array(image_rgb).tolist()

    return image_ascii, colors


def convert_folder(folder: str):
    for image_name in filter(
            lambda name: name.split(".")[-1] in ["jpg", "png"],
            os.listdir(folder)
    ):
        image = Image.open(os.path.join(folder, image_name))
        ascii_image = convert_brightness(image, target_width=64)
        with open(os.path.join(folder, f"{image_name}.txt"), "w+") as f:
            print(*ascii_image, sep="\n", file=f)


if __name__ == '__main__':
    convert_folder("images")
