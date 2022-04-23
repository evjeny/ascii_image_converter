import argparse
import json
import string
import typing

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def get_printable_chars():
    def _is_allowed(symbol: str) -> bool:
        if symbol == " ":
            return True
        return not symbol.isspace()

    non_whitespace = filter(_is_allowed, string.printable)
    return "".join(non_whitespace)


def get_text_dimensions(text_string: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    if text_string.isspace():
        return 5, 5

    return font.getmask(text_string).getbbox()[2:4]


def get_symbol_brightness(symbol: str, font: ImageFont.ImageFont) -> float:
    canvas_width, canvas_height = get_text_dimensions(symbol, font)
    canvas_width, canvas_height = canvas_width + 10, canvas_height + 10

    mean_empty_brightness = 255

    canvas = Image.new("L", (canvas_width, canvas_height), color=mean_empty_brightness)
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), symbol, font=font)

    text_width, text_height = draw.textsize(symbol, font=font)
    text_width, text_height = min(canvas_width, text_width), min(canvas_height, text_height)

    image_array = np.array(canvas)
    mean_brightness = np.mean(image_array[:text_height, :text_width])

    return mean_brightness / mean_empty_brightness


def normalize_array(array: list[float]) -> list[float]:
    min_value = min(array)
    max_value = max(array)
    return [(v - min_value) / (max_value - min_value) for v in array]


def main(font_paths: list[str], output: typing.Optional[str]):
    symbols = get_printable_chars()

    font_brightnesses: list[list[float]] = []
    for path in font_paths:
        font = ImageFont.truetype(path, size=20)
        print(f"Evaluating {path}")

        brightnesses = [get_symbol_brightness(s, font) for s in symbols]
        normalized_brightnesses = normalize_array(brightnesses)
        font_brightnesses.append(
            normalized_brightnesses
        )

    mean_brightnesses = np.mean(font_brightnesses, axis=0)
    mapping = {
        symbol: float(brightness) for symbol, brightness in zip(symbols, mean_brightnesses)
    }

    if not output:
        print(mapping)
    else:
        with open(output, "w+") as f:
            json.dump(mapping, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Get brightness mapping from fonts")
    parser.add_argument(
        "--font", type=str, nargs="+",
        help="paths to TrueType or OpenType fonts, if more than one provided, values will be averaged"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="path to output file, prints to stdout by default"
    )
    args = parser.parse_args()

    main(args.font, args.output)
