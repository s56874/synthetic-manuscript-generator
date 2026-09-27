import random


# ============================================================
# LAYOUT TYPES
# ============================================================

LAYOUT_TYPES = [
    "single_column",
    "two_block",
    "marginal",
    "centered",
]


# ============================================================
# CREATE MAIN TEXT BLOCK
# ============================================================

def create_main_block(
    image_width,
    image_height,
    min_margin=100,
    max_margin=160
):

    left = random.randint(
        min_margin,
        max_margin
    )

    right = random.randint(
        min_margin,
        max_margin
    )

    top = random.randint(
        min_margin,
        max_margin
    )

    bottom = random.randint(
        min_margin,
        max_margin
    )

    return {
        "type": "main_text",
        "x": left,
        "y": top,
        "width": image_width - left - right,
        "height": image_height - top - bottom,
    }


# ============================================================
# CREATE MARGINAL AREA
# ============================================================

def create_margin_block(
    main_block,
    image_width,
    image_height
):

    side = random.choice(
        [
            "left",
            "right"
        ]
    )

    margin_width = random.randint(
        90,
        180
    )

    if side == "left":

        x = random.randint(
            25,
            max(
                30,
                main_block["x"] - margin_width
            )
        )

    else:

        x = (
            main_block["x"]
            + main_block["width"]
            + random.randint(
                15,
                35
            )
        )

        if x + margin_width > image_width - 20:

            x = max(
                20,
                image_width
                - margin_width
                - 20
            )

    y = random.randint(
        main_block["y"] + 20,
        main_block["y"] + 120
    )

    height = random.randint(
        180,
        450
    )

    height = min(
        height,
        image_height - y - 20
    )

    return {
        "type": "marginal",
        "side": side,
        "x": x,
        "y": y,
        "width": margin_width,
        "height": height,
    }


# ============================================================
# CREATE SECONDARY TEXT BLOCK
# ============================================================

def create_secondary_block(
    main_block
):

    # Put a smaller block below or beside
    # the main manuscript text.

    position = random.choice(
        [
            "bottom",
            "side"
        ]
    )

    if position == "bottom":

        x = main_block["x"] + random.randint(
            0,
            80
        )

        y = (
            main_block["y"]
            + main_block["height"]
            - random.randint(
                150,
                250
            )
        )

        width = int(
            main_block["width"]
            * random.uniform(
                0.45,
                0.75
            )
        )

        height = random.randint(
            100,
            180
        )

    else:

        x = (
            main_block["x"]
            + random.randint(
                20,
                80
            )
        )

        y = (
            main_block["y"]
            + random.randint(
                50,
                150
            )
        )

        width = int(
            main_block["width"]
            * random.uniform(
                0.25,
                0.40
            )
        )

        height = random.randint(
            120,
            250
        )

    return {
        "type": "secondary",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }


# ============================================================
# SECTION MARKER
# ============================================================

def create_section_marker(
    main_block
):

    marker_position = random.choice(
        [
            "top",
            "left",
            "center"
        ]
    )

    if marker_position == "top":

        x = (
            main_block["x"]
            + random.randint(
                50,
                max(
                    51,
                    main_block["width"] - 150
                )
            )
        )

        y = (
            main_block["y"]
            - random.randint(
                35,
                70
            )
        )

    elif marker_position == "left":

        x = (
            main_block["x"]
            - random.randint(
                35,
                70
            )
        )

        y = (
            main_block["y"]
            + random.randint(
                50,
                200
            )
        )

    else:

        x = (
            main_block["x"]
            + main_block["width"] // 2
        )

        y = (
            main_block["y"]
            - random.randint(
                30,
                60
            )
        )

    return {
        "type": "section_marker",
        "x": x,
        "y": y,
        "size": random.randint(
            12,
            24
        ),
    }


# ============================================================
# SAFE BLOCK
# ============================================================

def clamp_block(
    block,
    image_width,
    image_height
):

    x = max(
        10,
        int(block["x"])
    )

    y = max(
        10,
        int(block["y"])
    )

    width = max(
        20,
        int(block["width"])
    )

    height = max(
        20,
        int(block["height"])
    )

    if x + width > image_width - 10:

        width = (
            image_width
            - x
            - 10
        )

    if y + height > image_height - 10:

        height = (
            image_height
            - y
            - 10
        )

    block["x"] = x
    block["y"] = y
    block["width"] = max(
        20,
        width
    )
    block["height"] = max(
        20,
        height
    )

    return block


# ============================================================
# CREATE COMPLETE LAYOUT
# ============================================================

def create_layout(
    image_width,
    image_height,
    min_margin=100,
    max_margin=160,
    layout_type=None
):

    if layout_type is None:

        layout_type = random.choice(
            LAYOUT_TYPES
        )

    # --------------------------------------------------------
    # Main text area
    # --------------------------------------------------------

    main_block = create_main_block(
        image_width,
        image_height,
        min_margin,
        max_margin
    )

    main_block = clamp_block(
        main_block,
        image_width,
        image_height
    )

    blocks = [
        main_block
    ]

    # --------------------------------------------------------
    # Layout variation
    # --------------------------------------------------------

    if layout_type == "single_column":

        pass

    elif layout_type == "two_block":

        secondary = create_secondary_block(
            main_block
        )

        secondary = clamp_block(
            secondary,
            image_width,
            image_height
        )

        blocks.append(
            secondary
        )

    elif layout_type == "marginal":

        marginal = create_margin_block(
            main_block,
            image_width,
            image_height
        )

        marginal = clamp_block(
            marginal,
            image_width,
            image_height
        )

        blocks.append(
            marginal
        )

    elif layout_type == "centered":

        # Make the main text slightly narrower,
        # producing a centered manuscript composition.

        main_block["x"] = random.randint(
            170,
            230
        )

        main_block["width"] = random.randint(
            850,
            1100
        )

        main_block = clamp_block(
            main_block,
            image_width,
            image_height
        )

    # --------------------------------------------------------
    # Optional section marker
    # --------------------------------------------------------

    section_marker = None

    if random.random() < 0.70:

        section_marker = create_section_marker(
            main_block
        )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {
        "layout_type": layout_type,
        "blocks": blocks,
        "section_marker": section_marker,
    }


# ============================================================
# CHOOSE TEXT SIZE FOR BLOCK
# ============================================================

def get_block_text_settings(
    block,
    image_width,
    image_height
):

    block_width = block["width"]

    if block["type"] == "main_text":

        font_size = random.randint(
            34,
            42
        )

        line_spacing = random.randint(
            12,
            22
        )

    elif block["type"] == "marginal":

        font_size = random.randint(
            20,
            28
        )

        line_spacing = random.randint(
            8,
            14
        )

    else:

        font_size = random.randint(
            24,
            32
        )

        line_spacing = random.randint(
            10,
            18
        )

    return {
        "font_size": font_size,
        "line_spacing": line_spacing,
        "max_width": max(
            100,
            block_width - 30
        ),
    }


# ============================================================
# GET CONTENT AREA
# ============================================================

def get_content_area(block):

    padding_left = random.randint(
        10,
        25
    )

    padding_top = random.randint(
        10,
        25
    )

    padding_right = random.randint(
        10,
        25
    )

    padding_bottom = random.randint(
        10,
        25
    )

    return {
        "x": block["x"] + padding_left,
        "y": block["y"] + padding_top,
        "width": (
            block["width"]
            - padding_left
            - padding_right
        ),
        "height": (
            block["height"]
            - padding_top
            - padding_bottom
        ),
    }