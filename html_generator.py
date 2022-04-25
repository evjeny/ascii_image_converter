import os

from PIL import Image

from convert import convert_brightness_rgb


def generate_tag(
        ascii_image: list[str],
        colors: list[list[tuple[int, int, int]]]
) -> str:
    def _convert_symbol(symbol: str, color: tuple[int, int, int]) -> str:
        color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        return f'<span style="color:{color};">{symbol}</span>'

    tag_value = "\n".join(
        "".join(
            _convert_symbol(ascii_value, color_value)
            for ascii_value, color_value in zip(ascii_line, colors_line)
        )
        for ascii_line, colors_line in zip(ascii_image, colors)
    )

    return f"<pre>{tag_value}</pre>"


def get_styles(line_height: float = 0.8, background_color: str = "black") -> str:
    return f"pre {{ line-height: {line_height}; background-color: {background_color};}}"


def convert_folder(folder: str):
    for image_name in filter(
            lambda name: name.split(".")[-1] in ["jpg", "png"],
            os.listdir(folder)
    ):
        image = Image.open(os.path.join(folder, image_name))
        ascii_image, colors_image = convert_brightness_rgb(image, target_width=64)
        pre_tag = generate_tag(ascii_image, colors_image)
        styles = get_styles()

        with open(os.path.join(folder, f"{image_name}_colors.html"), "w+") as f:
            f.write(f"<html><head><style>{styles}</style></head><body>{pre_tag}</body></html>")


if __name__ == '__main__':
    convert_folder("images")
