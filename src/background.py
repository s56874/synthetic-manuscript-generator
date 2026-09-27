import random
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


# ============================================================
# HELPERS
# ============================================================

def smooth_noise(width, height, small_size):
    small = np.random.normal(
        0, 1, (small_size, small_size)
    ).astype(np.float32)

    noise = cv2.resize(
        small,
        (width, height),
        interpolation=cv2.INTER_CUBIC
    )

    noise = cv2.GaussianBlur(
        noise,
        (0, 0),
        8
    )

    return noise


def normalize_noise(noise):
    noise = noise - noise.min()

    maximum = noise.max()

    if maximum != 0:
        noise = noise / maximum

    return noise


# ============================================================
# AGED PAPER
# ============================================================

def create_aged_paper(width, height):

    # --------------------------------------------------------
    # Base color
    # Reference-like warm historical paper
    # --------------------------------------------------------

    base = np.zeros(
        (height, width, 3),
        dtype=np.float32
    )

    base[:, :] = [
        174,
        148,
        100
    ]

    # --------------------------------------------------------
    # LARGE NATURAL COLOR CLOUDS
    # --------------------------------------------------------

    large = smooth_noise(
        width,
        height,
        10
    )

    large = normalize_noise(large)

    # darker + lighter areas
    large_variation = (
        large - 0.5
    ) * 24

    base[:, :, 0] += large_variation
    base[:, :, 1] += large_variation * 0.75
    base[:, :, 2] += large_variation * 0.45

    # --------------------------------------------------------
    # MEDIUM PAPER TEXTURE
    # --------------------------------------------------------

    medium = smooth_noise(
        width,
        height,
        28
    )

    medium = normalize_noise(medium)

    medium_variation = (
        medium - 0.5
    ) * 11

    base[:, :, 0] += medium_variation
    base[:, :, 1] += medium_variation * 0.8
    base[:, :, 2] += medium_variation * 0.55

    # --------------------------------------------------------
    # FINE PAPER GRAIN
    # --------------------------------------------------------

    grain = np.random.normal(
        0,
        3.0,
        (height, width, 1)
    )

    base += grain

    # ========================================================
    # OLD WATER / MOISTURE STAINS
    # ========================================================

    stain_layer = np.zeros(
        (height, width),
        dtype=np.float32
    )

    number_of_stains = random.randint(
        8,
        14
    )

    for _ in range(number_of_stains):

        cx = random.randint(
            -100,
            width + 100
        )

        cy = random.randint(
            -80,
            height + 80
        )

        rx = random.randint(
            70,
            220
        )

        ry = random.randint(
            40,
            150
        )

        # elliptical soft stain
        yy, xx = np.ogrid[
            :height,
            :width
        ]

        distance = (
            ((xx - cx) / rx) ** 2
            +
            ((yy - cy) / ry) ** 2
        )

        stain = np.exp(
            -distance * 2.2
        )

        # irregular noise inside stain
        local_noise = smooth_noise(
            width,
            height,
            20
        )

        local_noise = normalize_noise(
            local_noise
        )

        stain *= (
            0.65
            +
            local_noise * 0.45
        )

        stain_layer = np.maximum(
            stain_layer,
            stain
        )

    # blur for natural absorption
    stain_layer = cv2.GaussianBlur(
        stain_layer,
        (0, 0),
        12
    )

    stain_layer = np.clip(
        stain_layer,
        0,
        1
    )

    # brown stain color
    stain_color = np.array(
        [
            112,
            82,
            48
        ],
        dtype=np.float32
    )

    stain_strength = (
        stain_layer[:, :, None]
        * 0.28
    )

    base = (
        base * (1 - stain_strength)
        +
        stain_color * stain_strength
    )

    # ========================================================
    # LIGHT DISCOLORED PATCHES
    # ========================================================

    light_patch = smooth_noise(
        width,
        height,
        7
    )

    light_patch = normalize_noise(
        light_patch
    )

    light_mask = np.clip(
        light_patch - 0.55,
        0,
        1
    )

    light_mask = cv2.GaussianBlur(
        light_mask,
        (0, 0),
        18
    )

    base += (
        light_mask[:, :, None]
        * 9
    )

    # ========================================================
    # DARK EDGE AGING
    # ========================================================

    yy, xx = np.mgrid[
        0:height,
        0:width
    ]

    distance_to_edge = np.minimum.reduce(
        [
            xx,
            width - 1 - xx,
            yy,
            height - 1 - yy
        ]
    )

    edge_strength = np.clip(
        1 -
        distance_to_edge / 130,
        0,
        1
    )

    edge_strength = edge_strength ** 1.5

    # irregular edge darkness
    edge_noise = smooth_noise(
        width,
        height,
        8
    )

    edge_noise = normalize_noise(
        edge_noise
    )

    edge_strength *= (
        0.75
        +
        edge_noise * 0.45
    )

    base[:, :, 0] -= (
        edge_strength * 17
    )

    base[:, :, 1] -= (
        edge_strength * 14
    )

    base[:, :, 2] -= (
        edge_strength * 9
    )

    # ========================================================
    # OLD CORNERS
    # ========================================================

    corner_strength = np.zeros(
        (height, width),
        dtype=np.float32
    )

    corner_radius = 170

    corners = [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1)
    ]

    for cx, cy in corners:

        distance = np.sqrt(
            (xx - cx) ** 2
            +
            (yy - cy) ** 2
        )

        corner = np.clip(
            1 -
            distance / corner_radius,
            0,
            1
        )

        corner_strength = np.maximum(
            corner_strength,
            corner
        )

    base[:, :, 0] -= (
        corner_strength * 12
    )

    base[:, :, 1] -= (
        corner_strength * 9
    )

    base[:, :, 2] -= (
        corner_strength * 6
    )

    # ========================================================
    # CONVERT TO IMAGE
    # ========================================================

    base = np.clip(
        base,
        0,
        255
    ).astype(np.uint8)

    image = Image.fromarray(
        base,
        "RGB"
    )

    # ========================================================
    # PHYSICAL PAPER DETAILS
    # ========================================================

    overlay = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        overlay,
        "RGBA"
    )

    # ========================================================
    # NATURAL AGE SPOTS
    # ========================================================

    for _ in range(
        random.randint(180, 280)
    ):

        x = random.randint(
            5,
            width - 5
        )

        y = random.randint(
            5,
            height - 5
        )

        radius = random.choices(
            [1, 2, 3, 4, 5, 7],
            weights=[
                35,
                30,
                18,
                10,
                5,
                2
            ]
        )[0]

        alpha = random.randint(
            18,
            55
        )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(
                83,
                59,
                35,
                alpha
            )
        )

    # ========================================================
    # VERY SMALL PAPER FIBERS
    # ========================================================

    for _ in range(
        random.randint(
            700,
            1100
        )
    ):

        x = random.randint(
            0,
            width - 1
        )

        y = random.randint(
            0,
            height - 1
        )

        length = random.randint(
            4,
            24
        )

        angle = random.choice(
            [-1, 0, 1]
        )

        alpha = random.randint(
            12,
            32
        )

        draw.line(
            [
                (x, y),
                (
                    min(
                        width - 1,
                        x + length
                    ),
                    max(
                        0,
                        min(
                            height - 1,
                            y + angle
                        )
                    )
                )
            ],
            fill=(
                87,
                64,
                39,
                alpha
            ),
            width=1
        )

    # ========================================================
    # LIGHT PAPER FIBERS
    # ========================================================

    for _ in range(
        random.randint(
            350,
            550
        )
    ):

        x = random.randint(
            0,
            width - 1
        )

        y = random.randint(
            0,
            height - 1
        )

        length = random.randint(
            5,
            28
        )

        draw.line(
            [
                (x, y),
                (
                    min(
                        width - 1,
                        x + length
                    ),
                    y
                )
            ],
            fill=(
                226,
                201,
                157,
                random.randint(
                    12,
                    25
                )
            ),
            width=1
        )

    # ========================================================
    # FOLD / CREASES
    # ========================================================

    number_of_folds = random.randint(
        2,
        4
    )

    for _ in range(number_of_folds):

        horizontal = (
            random.random() < 0.7
        )

        if horizontal:

            y0 = random.randint(
                100,
                height - 100
            )

            points = []

            for x in range(
                -50,
                width + 50,
                20
            ):

                y = (
                    y0
                    +
                    random.randint(
                        -3,
                        3
                    )
                )

                points.append(
                    (x, y)
                )

        else:

            x0 = random.randint(
                100,
                width - 100
            )

            points = []

            for y in range(
                -50,
                height + 50,
                20
            ):

                x = (
                    x0
                    +
                    random.randint(
                        -3,
                        3
                    )
                )

                points.append(
                    (x, y)
                )

        # dark side of crease
        draw.line(
            points,
            fill=(
                82,
                58,
                35,
                random.randint(
                    22,
                    40
                )
            ),
            width=random.choice(
                [1, 1, 2]
            )
        )

        # bright side
        highlight_points = []

        for x, y in points:

            if horizontal:
                highlight_points.append(
                    (x, y + 2)
                )
            else:
                highlight_points.append(
                    (x + 2, y)
                )

        draw.line(
            highlight_points,
            fill=(
                230,
                205,
                160,
                random.randint(
                    15,
                    30
                )
            ),
            width=1
        )

    # ========================================================
    # FAINT WATER RINGS
    # ========================================================

    for _ in range(
        random.randint(
            2,
            5
        )
    ):

        cx = random.randint(
            80,
            width - 80
        )

        cy = random.randint(
            80,
            height - 80
        )

        rx = random.randint(
            60,
            150
        )

        ry = random.randint(
            25,
            80
        )

        draw.ellipse(
            (
                cx - rx,
                cy - ry,
                cx + rx,
                cy + ry
            ),
            outline=(
                105,
                78,
                46,
                random.randint(
                    18,
                    30
                )
            ),
            width=2
        )

    # ========================================================
    # SOFTEN PHYSICAL DETAILS
    # ========================================================

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(
            0.35
        )
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )

    # ========================================================
    # FINAL PAPER GRAIN
    # ========================================================

    array = np.array(
        image.convert("RGB")
    ).astype(np.float32)

    final_grain = np.random.normal(
        0,
        1.5,
        (height, width, 1)
    )

    array += final_grain

    array = np.clip(
        array,
        0,
        255
    ).astype(np.uint8)

    return Image.fromarray(
        array,
        "RGB"
    )


# ============================================================
# PALM LEAF
# ============================================================

def create_palm_leaf(width, height):

    base = np.zeros(
        (height, width, 3),
        dtype=np.float32
    )

    base[:, :] = [
        145,
        118,
        68
    ]

    # broad variation
    large = smooth_noise(
        width,
        height,
        10
    )

    large = normalize_noise(
        large
    )

    base += (
        large[:, :, None] - 0.5
    ) * 25

    # grain
    grain = np.random.normal(
        0,
        2.5,
        (height, width, 1)
    )

    base += grain

    base = np.clip(
        base,
        0,
        255
    ).astype(np.uint8)

    image = Image.fromarray(
        base,
        "RGB"
    )

    overlay = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(
        overlay,
        "RGBA"
    )

    # Palm leaf fibers
    for _ in range(
        random.randint(
            400,
            650
        )
    ):

        x = random.randint(
            0,
            width - 1
        )

        y = random.randint(
            0,
            height - 1
        )

        length = random.randint(
            30,
            180
        )

        draw.line(
            (
                x,
                y,
                min(
                    width - 1,
                    x + length
                ),
                y + random.randint(
                    -2,
                    2
                )
            ),
            fill=(
                67,
                45,
                25,
                random.randint(
                    12,
                    30
                )
            ),
            width=1
        )

    overlay = overlay.filter(
        ImageFilter.GaussianBlur(
            0.25
        )
    )

    image = Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )

    return image.convert("RGB")


# ============================================================
# MAIN BACKGROUND FUNCTION
# ============================================================

def create_background(
    width,
    height,
    background_type
):

    if background_type == "aged_paper":

        return create_aged_paper(
            width,
            height
        )

    if background_type == "palm_leaf":

        return create_palm_leaf(
            width,
            height
        )

    raise ValueError(
        f"Unknown background type: "
        f"{background_type}"
    )