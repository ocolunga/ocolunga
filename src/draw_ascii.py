import requests
from github import Github
from PIL import Image
from io import BytesIO
from src.fetch_info import fetch_stats
import json


def get_ascii_char(pixel):
    ascii_chars = ".:-=+*#%@"
    brightness = sum(pixel) / 3
    char_index = min(
        int(brightness / 255 * (len(ascii_chars) - 1)), len(ascii_chars) - 1
    )
    return ascii_chars[char_index]


def image_to_ascii(image, width=50) -> str:
    aspect_ratio = image.width / image.height
    height = int((width * aspect_ratio) * 0.5)

    image = image.resize((width, height))
    image = image.convert("RGB")
    ascii_str = ""

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            ascii_str += get_ascii_char(pixel)
        ascii_str += "\n"

    return ascii_str


def generate_logo(g: Github) -> str:
    with open("config.json", "r") as f:
        config = json.load(f)

    if config.get("custom_image_url"):
        image_url = config["custom_image_url"]
    else:
        image_url = g.get_user().avatar_url

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    return image_to_ascii(img)
