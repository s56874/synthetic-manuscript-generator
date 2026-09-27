import random
import numpy as np

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance


# ---------------------------------------------------------
# Random helpers
# ---------------------------------------------------------

def random_ink_color():
    """
    Return a natural dark-brown manuscript ink color.
    """
    colors = [
        (55, 38, 25),
        (62, 40, 25),
        (70, 43, 26),
        (78, 48, 28),
        (85, 52, 30),
    ]

    return random.choice(colors)


# ---------------------------------------------------------
# Ink fading
# ---------------------------------------------------------

def add_ink_fading(image, strength=0.10):
    """
    Add very subtle random fading to the whole image.
    Keeps text readable.
    """

    img = np.array(image).astype(np.float32)

    h, w = img.shape[:2]

    # Low-frequency random mask
    small_h = max(8, h // 80)
    small_w = max(8, w // 80)

    noise = np.random.normal(
        0,
        1,
        (small_h, small_w)
    ).astype(np.float32)

    noise_img = Image.fromarray(
        ((noise - noise.min()) /
         (noise.max() - noise.min() + 1e-6) * 255).astype(np.uint8)
    )

    noise_img = noise_img.resize(
        (w, h),
        Image.Resampling.BICUBIC
    )

    mask = np.array(noise_img).astype(np.float32) / 255.0

    # Only subtle variation
    factor = 1.0 - (mask - 0.5) * strength

    img *= factor[:, :, None]

    img = np.clip(img, 0, 255).astype(np.uint8)

    return Image.fromarray(img)


# ---------------------------------------------------------
# Water / moisture stains
# ---------------------------------------------------------

def add_water_stains(image, count=None):
    """
    Add subtle irregular moisture stains.
    """

    if count is None:
        count = random.randint(3, 7)

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    for _ in range(count):

        x = random.randint(0, width)
        y = random.randint(0, height)

        rx = random.randint(40, 150)
        ry = random.randint(20, 90)

        color = (
            random.randint(70, 110),
            random.randint(45, 70),
            random.randint(25, 45),
            random.randint(15, 35)
        )

        draw.ellipse(
            (
                x - rx,
                y - ry,
                x + rx,
                y + ry
            ),
            fill=color
        )

    # Strong blur makes stains look natural
    overlay = overlay.filter(
        ImageFilter.GaussianBlur(18)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


# ---------------------------------------------------------
# Small age spots
# ---------------------------------------------------------

def add_age_spots(image, count=None):
    """
    Add small irregular age spots.
    """

    if count is None:
        count = random.randint(60, 140)

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    for _ in range(count):

        x = random.randint(5, width - 5)
        y = random.randint(5, height - 5)

        radius = random.choice([
            1, 1, 2, 2, 3, 4, 5
        ])

        alpha = random.randint(15, 55)

        color = (
            random.randint(75, 115),
            random.randint(50, 75),
            random.randint(30, 50),
            alpha
        )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=color
        )

    # Slight softening
    overlay = overlay.filter(
        ImageFilter.GaussianBlur(0.5)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


# ---------------------------------------------------------
# Fold shadows
# ---------------------------------------------------------

def add_fold_shadows(image, count=None):
    """
    Add very subtle vertical/horizontal fold shadows.
    """

    if count is None:
        count = random.randint(1, 3)

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    for _ in range(count):

        if random.random() < 0.5:

            # Vertical fold
            x = random.randint(
                int(width * 0.15),
                int(width * 0.85)
            )

            fold_width = random.randint(8, 25)

            draw.rectangle(
                (
                    x - fold_width,
                    0,
                    x + fold_width,
                    height
                ),
                fill=(60, 40, 25, random.randint(8, 20))
            )

        else:

            # Horizontal fold
            y = random.randint(
                int(height * 0.15),
                int(height * 0.85)
            )

            fold_height = random.randint(8, 20)

            draw.rectangle(
                (
                    0,
                    y - fold_height,
                    width,
                    y + fold_height
                ),
                fill=(60, 40, 25, random.randint(8, 20))
            )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(8)
    )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


# ---------------------------------------------------------
# Edge aging
# ---------------------------------------------------------

def add_edge_aging(image, strength=0.18):
    """
    Darken edges slightly to simulate long-term handling.
    """

    img = np.array(image).astype(np.float32)

    h, w = img.shape[:2]

    yy, xx = np.mgrid[0:h, 0:w]

    # Distance from center
    dx = np.abs(xx - w / 2) / (w / 2)
    dy = np.abs(yy - h / 2) / (h / 2)

    edge = np.maximum(dx, dy)

    # Only affect outer area
    edge_mask = np.clip(
        (edge - 0.55) / 0.45,
        0,
        1
    )

    factor = 1.0 - edge_mask * strength

    img *= factor[:, :, None]

    img = np.clip(img, 0, 255).astype(np.uint8)

    return Image.fromarray(img)


# ---------------------------------------------------------
# Paper scratches / fibers
# ---------------------------------------------------------

def add_paper_fibers(image, count=None):
    """
    Add very thin natural paper fibers.
    """

    if count is None:
        count = random.randint(30, 80)

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    width, height = image.size

    for _ in range(count):

        x = random.randint(0, width)
        y = random.randint(0, height)

        length = random.randint(10, 70)

        color = (
            random.randint(70, 110),
            random.randint(50, 80),
            random.randint(30, 50),
            random.randint(10, 35)
        )

        draw.line(
            (
                x,
                y,
                x + length,
                y + random.randint(-2, 2)
            ),
            fill=color,
            width=1
        )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    ).convert("RGB")


# ---------------------------------------------------------
# Final subtle contrast
# ---------------------------------------------------------

def enhance_manuscript(image):
    """
    Final enhancement.
    """

    image = ImageEnhance.Contrast(
        image
    ).enhance(1.04)

    image = ImageEnhance.Sharpness(
        image
    ).enhance(1.08)

    return image


# ---------------------------------------------------------
# MAIN ARTIFACT PIPELINE
# ---------------------------------------------------------

def apply_artifacts(image):
    """
    Apply all historical manuscript artifacts.

    Order is important:
        age spots
        moisture
        fibers
        folds
        edge aging
        fading
        enhancement
    """

    image = add_age_spots(image)

    image = add_water_stains(image)

    image = add_paper_fibers(image)

    image = add_fold_shadows(image)

    image = add_edge_aging(image)

    image = add_ink_fading(image, strength=0.07)

    image = enhance_manuscript(image)

    return image