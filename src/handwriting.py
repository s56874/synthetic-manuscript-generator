from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os
import random
import re
import json


# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FONT_PATH = os.path.join(
    BASE_DIR,
    "fonts",
    "devanagari",
    "NotoSansDevanagari-Regular.ttf.ttf"
)

TEXT_PATH = os.path.join(
    BASE_DIR,
    "texts",
    "devanagari_md.md"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output",
    "devanagari"
)


# ==================================================
# OLD MANUSCRIPT PAPER
# ==================================================

def create_old_paper(width, height):

    # Base ancient paper color
    paper = np.zeros(
        (height, width, 3),
        dtype=np.float32
    )

    paper[:, :, 0] = 190
    paper[:, :, 1] = 165
    paper[:, :, 2] = 115

    # Natural paper noise
    noise = np.random.normal(
        0,
        10,
        (height, width, 1)
    )

    paper = paper + noise

    paper = np.clip(
        paper,
        0,
        255
    )

    paper = paper.astype(
        np.uint8
    )

    image = Image.fromarray(
        paper,
        "RGB"
    )

    # Add all old-paper effects
    image = add_uneven_aging(image)
    image = add_faded_areas(image)
    image = add_water_stains(image)
    image = add_old_edges(image)
    image = add_age_spots(image)
    image = add_fibers(image)
    image = add_wrinkles(image)
    image = add_worn_edges(image)

    return image


# ==================================================
# UNEVEN AGING
# ==================================================

def add_uneven_aging(image):

    width, height = image.size

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    for _ in range(35):

        x = random.randint(
            -100,
            width
        )

        y = random.randint(
            -100,
            height
        )

        w = random.randint(
            80,
            350
        )

        h = random.randint(
            60,
            250
        )

        color = random.choice([
            (90, 55, 25, 20),
            (110, 70, 30, 25),
            (70, 45, 20, 18),
            (145, 105, 55, 18)
        ])

        draw.ellipse(
            (
                x,
                y,
                x + w,
                y + h
            ),
            fill=color
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(40)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        layer
    )


# ==================================================
# FADED AREAS
# ==================================================

def add_faded_areas(image):

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    width, height = image.size

    for _ in range(12):

        x = random.randint(
            0,
            width
        )

        y = random.randint(
            0,
            height
        )

        radius = random.randint(
            60,
            180
        )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(
                225,
                205,
                155,
                random.randint(
                    8,
                    25
                )
            )
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(35)
    )

    return Image.alpha_composite(
        image,
        layer
    )


# ==================================================
# WATER STAINS
# ==================================================

def add_water_stains(image):

    width, height = image.size

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    for _ in range(12):

        x = random.randint(
            -50,
            width
        )

        y = random.randint(
            -50,
            height
        )

        w = random.randint(
            60,
            220
        )

        h = random.randint(
            40,
            150
        )

        draw.ellipse(
            (
                x,
                y,
                x + w,
                y + h
            ),
            outline=(
                85,
                55,
                25,
                random.randint(
                    20,
                    55
                )
            ),
            width=random.randint(
                2,
                6
            )
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(5)
    )

    return Image.alpha_composite(
        image,
        layer
    )


# ==================================================
# DARK OLD EDGES
# ==================================================

def add_old_edges(image):

    width, height = image.size

    array = np.array(
        image.convert("RGBA")
    )

    for y in range(height):

        for x in range(width):

            distance = min(
                x,
                y,
                width - x,
                height - y
            )

            if distance < 110:

                strength = (
                    110 - distance
                ) / 110

                alpha = strength * 0.30

                pixel = (
                    array[y, x, :3]
                    .astype(np.float32)
                )

                brown = np.array([
                    65,
                    40,
                    20
                ])

                pixel = (
                    pixel * (1 - alpha)
                    +
                    brown * alpha
                )

                array[
                    y,
                    x,
                    :3
                ] = pixel

    return Image.fromarray(
        array.astype(np.uint8),
        "RGBA"
    )


# ==================================================
# OLD AGE SPOTS
# ==================================================

def add_age_spots(image):

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    width, height = image.size

    for _ in range(650):

        x = random.randint(
            0,
            width
        )

        y = random.randint(
            0,
            height
        )

        radius = random.randint(
            1,
            4
        )

        color = random.choice([
            (65, 40, 20, 30),
            (80, 45, 20, 35),
            (100, 65, 30, 25),
            (50, 35, 20, 20)
        ])

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=color
        )

    return Image.alpha_composite(
        image,
        layer
    )


# ==================================================
# PAPER FIBERS
# ==================================================

def add_fibers(image):

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    width, height = image.size

    for _ in range(900):

        x = random.randint(
            0,
            width - 1
        )

        y = random.randint(
            0,
            height - 1
        )

        length = random.randint(
            2,
            12
        )

        draw.line(
            (
                x,
                y,
                x + length,
                y + random.randint(
                    -1,
                    1
                )
            ),
            fill=(
                70,
                50,
                30,
                random.randint(
                    10,
                    35
                )
            ),
            width=1
        )

    return Image.alpha_composite(
        image,
        layer
    )


# ==================================================
# OLD WRINKLES
# ==================================================

def add_wrinkles(image):

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    width, height = image.size

    # Vertical folds
    for _ in range(4):

        x = random.randint(
            100,
            width - 100
        )

        points = []

        for y in range(
            0,
            height,
            20
        ):

            points.append(
                (
                    x + random.randint(
                        -5,
                        5
                    ),
                    y
                )
            )

        draw.line(
            points,
            fill=(
                65,
                40,
                20,
                35
            ),
            width=2
        )

    # Horizontal folds
    for _ in range(3):

        y = random.randint(
            100,
            height - 100
        )

        points = []

        for x in range(
            0,
            width,
            20
        ):

            points.append(
                (
                    x,
                    y + random.randint(
                        -4,
                        4
                    )
                )
            )

        draw.line(
            points,
            fill=(
                65,
                40,
                20,
                30
            ),
            width=2
        )

    layer = layer.filter(
        ImageFilter.GaussianBlur(1.5)
    )

    return Image.alpha_composite(
        image,
        layer
    )


# ==================================================
# WORN EDGES
# ==================================================

def add_worn_edges(image):

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    width, height = image.size

    for _ in range(200):

        side = random.choice([
            "left",
            "right",
            "top",
            "bottom"
        ])

        if side == "left":

            x = random.randint(
                0,
                25
            )

            y = random.randint(
                0,
                height
            )

        elif side == "right":

            x = random.randint(
                width - 25,
                width
            )

            y = random.randint(
                0,
                height
            )

        elif side == "top":

            x = random.randint(
                0,
                width
            )

            y = random.randint(
                0,
                25
            )

        else:

            x = random.randint(
                0,
                width
            )

            y = random.randint(
                height - 25,
                height
            )

        radius = random.randint(
            1,
            7
        )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(
                55,
                35,
                15,
                random.randint(
                    25,
                    70
                )
            )
        )

    return Image.alpha_composite(
        image,
        layer
    )


# ==================================================
# READ TEXT
# ==================================================

def read_text():

    with open(
        TEXT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n+",
        " ",
        text
    )

    return text.strip()


# ==================================================
# CREATE WORD
# ==================================================

def create_word(word):

    font_size = random.randint(
        30,
        35
    )

    font = ImageFont.truetype(
        FONT_PATH,
        font_size
    )

    temp = Image.new(
        "RGBA",
        (500, 100),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(temp)

    # Natural ink variation
    if random.random() < 0.15:

        ink = (
            random.randint(90, 140),
            random.randint(40, 75),
            random.randint(20, 45),
            random.randint(180, 230)
        )

    else:

        ink = (
            random.randint(25, 65),
            random.randint(18, 45),
            random.randint(10, 30),
            random.randint(190, 240)
        )

    bbox = draw.textbbox(
        (0, 0),
        word,
        font=font
    )

    word_width = (
        bbox[2] - bbox[0]
    )

    word_height = (
        bbox[3] - bbox[1]
    )

    draw.text(
        (10, 10),
        word,
        font=font,
        fill=ink
    )

    temp = temp.crop(
        (
            5,
            5,
            word_width + 15,
            word_height + 15
        )
    )

    # Slight writing angle
    angle = random.uniform(
        -2.0,
        2.0
    )

    temp = temp.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=True
    )

    # Slight ink softness
    if random.random() < 0.25:

        temp = temp.filter(
            ImageFilter.GaussianBlur(
                random.uniform(
                    0.1,
                    0.35
                )
            )
        )

    return temp


# ==================================================
# MAKE TEXT LINES
# ==================================================

def make_lines(
    text,
    font_size=34,
    max_width=1000
):

    font = ImageFont.truetype(
        FONT_PATH,
        font_size
    )

    words = text.split()

    lines = []

    current_line = []

    current_width = 0

    for word in words:

        bbox = font.getbbox(
            word
        )

        word_width = (
            bbox[2] - bbox[0]
        )

        space_width = 15

        if (
            current_width +
            word_width +
            space_width
            > max_width
        ):

            if current_line:

                lines.append(
                    current_line
                )

            current_line = [
                word
            ]

            current_width = (
                word_width
            )

        else:

            current_line.append(
                word
            )

            current_width += (
                word_width +
                space_width
            )

    if current_line:

        lines.append(
            current_line
        )

    return lines


# ==================================================
# CREATE MANUSCRIPT
# ==================================================

def create_manuscript(
    image_number=1,
    split="train"
):

    width = 1200
    height = 800

    # ----------------------------------------------
    # CREATE OLD PAGE DIRECTLY HERE
    # ----------------------------------------------

    image = create_old_paper(
        width,
        height
    )

    image = image.convert(
        "RGBA"
    )

    # ----------------------------------------------
    # SOURCE TEXT
    # ----------------------------------------------

    text = read_text()

    left = 85
    right = 100
    top = 65
    bottom = 65

    lines = make_lines(
        text,
        font_size=34,
        max_width=(
            width -
            left -
            right
        )
    )

    y = top

    line_height = 53

    annotations = []

    # ----------------------------------------------
    # DRAW WORDS
    # ----------------------------------------------

    for line_number, line in enumerate(
        lines
    ):

        if y > height - bottom:
            break

        x = (
            left +
            random.randint(
                -3,
                4
            )
        )

        baseline = random.randint(
            -3,
            3
        )

        for word in line:

            word_image = create_word(
                word
            )

            # Never allow horizontal overflow
            if (
                x + word_image.width
                > width - right
            ):
                break

            word_y = (
                y +
                baseline +
                random.randint(
                    -2,
                    2
                )
            )

            # Draw word
            image.alpha_composite(
                word_image,
                (
                    x,
                    word_y
                )
            )

            # Ground truth box
            bbox = [
                int(x),
                int(word_y),
                int(
                    x +
                    word_image.width
                ),
                int(
                    word_y +
                    word_image.height
                )
            ]

            annotations.append({
                "text": word,
                "bbox": bbox,
                "line": line_number
            })

            x += (
                word_image.width +
                random.randint(
                    7,
                    16
                )
            )

        y += (
            line_height +
            random.randint(
                -3,
                5
            )
        )

    # ----------------------------------------------
    # VERY LIGHT FINAL SOFTNESS
    # ----------------------------------------------

    image = image.filter(
        ImageFilter.GaussianBlur(
            0.12
        )
    )

    # ----------------------------------------------
    # OUTPUT DIRECTORY
    # ----------------------------------------------

    split_dir = os.path.join(
        OUTPUT_DIR,
        split
    )

    os.makedirs(
        split_dir,
        exist_ok=True
    )

    # ----------------------------------------------
    # SAVE IMAGE
    # ----------------------------------------------

    image_name = (
        f"devanagari_{image_number:03d}.png"
    )

    image_path = os.path.join(
        split_dir,
        image_name
    )

    image.convert(
        "RGB"
    ).save(
        image_path,
        quality=95
    )

    # ----------------------------------------------
    # SAVE JSON
    # ----------------------------------------------

    annotation = {
        "image": image_name,
        "script": "devanagari",
        "split": split,
        "width": width,
        "height": height,
        "text": text,
        "words": annotations
    }

    annotation_name = (
        f"devanagari_{image_number:03d}.json"
    )

    annotation_path = os.path.join(
        split_dir,
        annotation_name
    )

    with open(
        annotation_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            annotation,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"Created {split}: "
        f"{image_name}"
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    create_manuscript(
        image_number=1,
        split="train"
    )