import argparse
import os
from typing import Optional

from PIL import Image

from brightness_levels import read_sorted_mapping
from convert import convert_brightness, convert_brightness_rgb
from html_generator import get_styles, generate_tag, generate_tag_rgb


def main(
        image_path: str,
        output_txt_path: Optional[str], output_html_path: Optional[str],
        target_width: Optional[int], target_height: Optional[int], use_rgb: bool,
        html_line_height: float, html_background_color: str, html_text_color: str,
        brightness_config_path: Optional[str]
):
    image = Image.open(image_path)
    brightness_config = read_sorted_mapping(brightness_config_path) if brightness_config_path else None

    if use_rgb:
        ascii_image, colors_image = convert_brightness_rgb(
            image=image, sorted_brightness_config=brightness_config,
            target_width=target_width, target_height=target_height
        )
        html_tag = generate_tag_rgb(ascii_image, colors_image)
    else:
        ascii_image = convert_brightness(
            image=image, sorted_brightness_config=brightness_config,
            target_width=target_width, target_height=target_height
        )
        html_tag = generate_tag(ascii_image)

    if output_txt_path:
        with open(output_txt_path, "w+") as f:
            print(*ascii_image, sep="\n", file=f)
    elif output_html_path:
        styles = get_styles(
            line_height=html_line_height,
            background_color=html_background_color,
            color=html_text_color
        )

        with open(output_html_path, "w+") as f:
            html_str = f"""
                <html>
                    <head>
                        <style>{styles}</style>
                    </head>
                    <body>
                        {html_tag}
                    </body>
                </html>"""
            f.write(html_str)
    else:
        raise Exception("Nothing was saved!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Get ascii from image")
    parser.add_argument("--image", type=str, required=True, help="path to image")
    parser.add_argument("--output_txt", type=str, default=None, help="path to save converted txt file")
    parser.add_argument("--output_html", type=str, default=None, help="path to save converted html file")
    parser.add_argument(
        "--target_width", type=int, default=None,
        help="target ascii art width, if not provided, image width is used"
    )
    parser.add_argument(
        "--target_height", type=int, default=None,
        help="target ascii art height, if not provided, image height is used"
    )
    parser.add_argument(
        "--rgb", action="store_true",
        help="whether use RGB encoding (useful only if --output_html provided)"
    )
    parser.add_argument(
        "--html_line_height", type=float, default=0.8,
        help="height of line of text in html file"
    )
    parser.add_argument(
        "--html_background_color", type=str, default="white",
        help="default html background CSS color"
    )
    parser.add_argument(
        "--html_text_color", type=str, default="black",
        help="default html text CSS color"
    )
    parser.add_argument(
        "--config", type=str, default=None,
        help="brightness config path, by default mean.json is used"
    )

    args = parser.parse_args()
    main(
        args.image, args.output_txt, args.output_html,
        args.target_width, args.target_height, args.rgb,
        args.html_line_height, args.html_background_color, args.html_text_color,
        args.config
    )
