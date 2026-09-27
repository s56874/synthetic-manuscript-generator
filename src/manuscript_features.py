import random

from PIL import ImageDraw


def draw_section_marker(
    image,
    x,
    y,
    size=12
):
    """
    Draw a simple manuscript-style section marker.
    This is a graphic marker, not invented text.
    """

    draw = ImageDraw.Draw(image)

    color = random.choice([
        (90, 45, 25),
        (110, 50, 25),
        (75, 40, 25)
    ])

    # Diamond
    points = [
        (x, y - size),
        (x + size, y),
        (x, y + size),
        (x - size, y)
    ]

    draw.polygon(
        points,
        fill=color
    )


def draw_small_marker(
    image,
    x,
    y,
    size=7
):
    """
    Small circular manuscript marker.
    """

    draw = ImageDraw.Draw(image)

    color = random.choice([
        (80, 40, 25),
        (100, 50, 25),
        (70, 35, 20)
    ])

    draw.ellipse(
        (
            x - size,
            y - size,
            x + size,
            y + size
        ),
        fill=color
    )


def draw_highlights(
    image,
    bounding_boxes,
    probability=0.15
):
    """
    Add subtle underline/highlight marks
    to some rendered text lines.
    """

    draw = ImageDraw.Draw(image)

    for box in bounding_boxes:

        if random.random() > probability:
            continue

        x1, y1, x2, y2 = box["bbox"]

        color = random.choice([
            (120, 65, 25),
            (140, 75, 30),
            (100, 55, 25)
        ])

        # Underline rather than covering the text.
        draw.line(
            (
                x1,
                y2 + 3,
                x2,
                y2 + 3
            ),
            fill=color,
            width=random.choice([1, 2])
        )


def draw_marginal_line(
    image,
    x,
    y1,
    y2
):
    """
    Draw a subtle vertical marginal separator.
    """

    draw = ImageDraw.Draw(image)

    color = random.choice([
        (110, 70, 40),
        (125, 75, 40),
        (95, 60, 35)
    ])

    draw.line(
        (x, y1, x, y2),
        fill=color,
        width=1
    )


def add_manuscript_features(
    image,
    bounding_boxes,
    region=None
):
    """
    Add visual manuscript features after text rendering.
    """

    image_width, image_height = image.size

    # --------------------------------
    # SECTION MARKER
    # --------------------------------

    if region is not None:

        marker_x = region["x"]

        marker_y = max(
            30,
            region["y"] - 35
        )

        draw_section_marker(
            image,
            marker_x,
            marker_y,
            size=random.randint(8, 14)
        )

    # --------------------------------
    # HIGHLIGHTED TEXT
    # --------------------------------

    draw_highlights(
        image,
        bounding_boxes,
        probability=0.12
    )

    return image