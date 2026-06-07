# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Fondo degradado azul/violeta
        for y in range(size):
            r = int(30 + (50 - 30) * y / size)
            g = int(30 + (40 - 30) * y / size)
            b = int(180 + (220 - 180) * y / size)
            draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

        # Bordes redondeados (esquinas transparentes)
        radius = size // 5
        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
        img.putalpha(mask)

        # Letras "MD"
        draw = ImageDraw.Draw(img)
        text = "MD"
        font_size = size // 3
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (size - tw) // 2
        y = (size - th) // 2
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

        images.append(img)

    out_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    images[0].save(out_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=images[1:])
    print(f"Icono creado: {out_path}")

if __name__ == "__main__":
    create_icon()
