# ascii_image_converter

Convert images to ASCII-art!

---

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run converter script

```bash
python convert_image.py --help

python convert_image.py \
  --image images/eva_small.jpg \
  --output_html eva_small.html \
  --rgb --target_width 120 \
  --config precomputed_mappings/arial.json
```

## Include into your code

```python
from PIL import Image

from convert import convert_brightness_rgb
from html_generator import  get_styles, generate_tag_rgb

image = Image.open("images/eva_small.jpg")
ascii_image, colors_image = convert_brightness_rgb(image, target_width=64)

with open("eva_small_ascii.txt", "w+") as f:
    print(*ascii_image, sep="\n", file=f)

with open("eva_small_ascii.html", "w+") as f:
    html_str = f"""
    <html>
        <head>
            <style>{get_styles()}</style>
        </head>
        <body>
            {generate_tag_rgb(ascii_image, colors_image)}
        </body>
    </html>"""
    f.write(html_str)
```

## Custom brightness config

Repo contains `brightness configs` (precomputed brightness levels for different character),
stored in [precomputed_mappings](precomputed_mappings/), `mean.json` config is used by default
(evaluated as mean brightness between Arial, JetBrainsMono-Regular and UbuntuMono-Regular)

To create custom config you can use [get_brightness_mapping.py](get_brightness_mapping.py):

```bash
get_brightness_mapping.py \
  --font /path/to/font/font1.ttf \
         /path/to/another/font/font2.ttf \
  --output new_config.json
```

Then this config can be used in code as:

```python
from PIL import Image

from brightness_levels import read_sorted_mapping
from convert import convert_brightness

# read new config
custom_config = read_sorted_mapping("new_config.json")

image = Image.open("images/eva_small.jpg")
ascii_image = convert_brightness(
    image,
    target_width=64,
    sorted_brightness_config=custom_config # use brightness levels from new config
)

with open("eva_small_ascii.txt", "w+") as f:
    print(*ascii_image, sep="\n", file=f)

```
