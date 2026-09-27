import random
import numpy as np

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageFilter,
)


# --------------------------------------------------
# Load font
# --------------------------------------------------

def load_font(font_path, font_size):

    return ImageFont.truetype(
        font_path,
        font_size
    )


# --------------------------------------------------
# Natural ink colors
# --------------------------------------------------

def random_ink_color():

    colors = [
        (48, 32, 21),
        (52, 34, 21),
        (57, 37, 22),
        (62, 39, 23),
        (68, 42, 24),
        (74, 45, 25),
        (80, 48, 27),
    ]

    return random.choice(colors)


# --------------------------------------------------
# Create text mask
# --------------------------------------------------

def create_ink_layer(
    text,
    font,
    padding=25
):

    temp = Image.new(
        "L",
        (3500, 500),
        0
    )

    draw = ImageDraw.Draw(
        temp
    )

    draw.text(
        (padding, padding),
        text,
        font=font,
        fill=255
    )

    bbox = temp.getbbox()

    if bbox is None:
        return None

    mask = temp.crop(
        bbox
    )

    return mask


# --------------------------------------------------
# Natural ink density variation
# --------------------------------------------------

def apply_ink_variation(mask):

    arr = np.array(
        mask
    ).astype(
        np.float32
    )

    h, w = arr.shape

    # Low-frequency variation
    small_h = max(
        4,
        h // 18
    )

    small_w = max(
        4,
        w // 18
    )

    noise = np.random.normal(
        0,
        1,
        (small_h, small_w)
    )

    noise = noise - noise.min()

    if noise.max() > 0:

        noise = noise / noise.max()

    noise = (
        noise * 2.0
    ) - 1.0

    noise_img = Image.fromarray(
        (
            (noise + 1.0)
            * 127.5
        ).astype(
            np.uint8
        )
    )

    noise_img = noise_img.resize(
        (w, h),
        Image.Resampling.BICUBIC
    )

    noise_arr = np.array(
        noise_img
    ).astype(
        np.float32
    )

    noise_arr = (
        noise_arr - 127.5
    ) / 127.5

    # Small ink-density changes
    arr = arr + (
        noise_arr * 20
    )

    arr = np.clip(
        arr,
        0,
        255
    )

    return Image.fromarray(
        arr.astype(np.uint8),
        mode="L"
    )


# --------------------------------------------------
# Small ink bleeding
# --------------------------------------------------

def add_subtle_bleed(mask):

    radius = random.uniform(
        0.15,
        0.45
    )

    return mask.filter(
        ImageFilter.GaussianBlur(
            radius
        )
    )


# --------------------------------------------------
# Occasional faded ink
# --------------------------------------------------

def add_fading(mask):

    if random.random() > 0.30:

        return mask

    arr = np.array(
        mask
    ).astype(
        np.float32
    )

    h, w = arr.shape

    # Create gentle horizontal fading
    fade = np.ones(
        (h, w),
        dtype=np.float32
    )

    fade_start = random.randint(
        0,
        max(0, w // 3)
    )

    fade_width = random.randint(
        max(20, w // 8),
        max(30, w // 3)
    )

    end = min(
        w,
        fade_start + fade_width
    )

    if end > fade_start:

        fade_values = np.linspace(
            1.0,
            random.uniform(
                0.65,
                0.90
            ),
            end - fade_start
        )

        fade[
            :,
            fade_start:end
        ] *= fade_values

    arr *= fade

    return Image.fromarray(
        np.clip(
            arr,
            0,
            255
        ).astype(
            np.uint8
        ),
        mode="L"
    )


# --------------------------------------------------
# Slight handwritten slant
# --------------------------------------------------

def apply_slant(
    image,
    max_shear=0.025
):

    shear = random.uniform(
        -max_shear,
        max_shear
    )

    w, h = image.size

    shift = abs(
        shear * h
    )

    new_width = int(
        w + shift
    )

    if shear >= 0:

        data = (
            1,
            shear,
            -shift,
            0,
            1,
            0
        )

    else:

        data = (
            1,
            shear,
            0,
            0,
            1,
            0
        )

    return image.transform(
        (new_width, h),
        Image.Transform.AFFINE,
        data,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0)
    )


# --------------------------------------------------
# Tiny width variation
# --------------------------------------------------

def apply_scale_variation(
    image
):

    scale_x = random.uniform(
        0.985,
        1.015
    )

    scale_y = random.uniform(
        0.990,
        1.010
    )

    w, h = image.size

    new_w = max(
        1,
        int(w * scale_x)
    )

    new_h = max(
        1,
        int(h * scale_y)
    )

    return image.resize(
        (new_w, new_h),
        Image.Resampling.BICUBIC
    )


# --------------------------------------------------
# Transform one handwritten line
# --------------------------------------------------

def transform_text_line(
    line_image
):

    # Tiny horizontal scaling
    line_image = apply_scale_variation(
        line_image
    )

    # Slight handwriting slant
    line_image = apply_slant(
        line_image,
        max_shear=0.018
    )

    # Tiny rotation
    angle = random.uniform(
        -0.65,
        0.65
    )

    line_image = line_image.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=True,
        fillcolor=(0, 0, 0, 0)
    )

    return line_image


# --------------------------------------------------
# Convert mask to colored ink
# --------------------------------------------------

def mask_to_ink(mask):

    color = random_ink_color()

    rgba = Image.new(
        "RGBA",
        mask.size,
        (
            color[0],
            color[1],
            color[2],
            0
        )
    )

    rgba.putalpha(
        mask
    )

    return rgba


# --------------------------------------------------
# Render one line
# --------------------------------------------------

def render_single_line(
    text,
    font,
    ink_strength=True
):

    mask = create_ink_layer(
        text,
        font
    )

    if mask is None:
        return None

    # Ink density
    if ink_strength:

        mask = apply_ink_variation(
            mask
        )

    # Occasional fading
    mask = add_fading(
        mask
    )

    # Slight bleeding
    mask = add_subtle_bleed(
        mask
    )

    # Convert to brown ink
    ink = mask_to_ink(
        mask
    )

    # Handwritten transformation
    ink = transform_text_line(
        ink
    )

    return ink


# --------------------------------------------------
# Wrap text
# --------------------------------------------------

def wrap_text(
    text,
    font,
    max_width,
    draw=None
):

    if draw is None:

        temp = Image.new(
            "RGB",
            (10, 10)
        )

        draw = ImageDraw.Draw(
            temp
        )

    words = text.split()

    lines = []

    current = ""

    for word in words:

        candidate = (
            word
            if not current
            else current + " " + word
        )

        bbox = draw.textbbox(
            (0, 0),
            candidate,
            font=font
        )

        width = (
            bbox[2] - bbox[0]
        )

        if width <= max_width:

            current = candidate

        else:

            if current:

                lines.append(
                    current
                )

            current = word

    if current:

        lines.append(
            current
        )

    return lines


# --------------------------------------------------
# Render complete text
# --------------------------------------------------

def render_text(
    image,
    text=None,
    lines=None,
    font_path=None,
    font_size=42,
    x=120,
    y=120,
    max_width=None,
    max_height=None,
    line_spacing=25,
):

    if text is None and lines is None:

        raise ValueError(
            "Provide either 'text' or 'lines'."
        )

    if font_path is None:

        raise ValueError(
            "font_path is required."
        )

    font = load_font(
        font_path,
        font_size
    )

    draw = ImageDraw.Draw(
        image
    )

    image_width, image_height = (
        image.size
    )

    if max_width is None:

        max_width = (
            image_width
            - x
            - 100
        )

    if max_height is None:

        max_height = (
            image_height
            - y
            - 100
        )

    # Create wrapped lines
    if lines is None:

        lines = wrap_text(
            text,
            font,
            max_width,
            draw
        )

    bounding_boxes = []

    current_y = y

    for line_index, line in enumerate(
        lines
    ):

        if not line.strip():

            continue

        # Render handwritten line
        line_image = render_single_line(
            line,
            font
        )

        if line_image is None:

            continue

        lw, lh = (
            line_image.size
        )

        # Safety scaling
        if lw > max_width:

            scale = (
                max_width / lw
            )

            new_w = int(
                lw * scale
            )

            new_h = int(
                lh * scale
            )

            line_image = line_image.resize(
                (new_w, new_h),
                Image.Resampling.LANCZOS
            )

            lw, lh = (
                line_image.size
            )

        # Small handwritten position variation
        x_offset = random.randint(
            -4,
            4
        )

        y_offset = random.randint(
            -3,
            3
        )

        paste_x = (
            x + x_offset
        )

        paste_y = (
            current_y + y_offset
        )

        # Keep inside image
        if paste_x < 10:

            paste_x = 10

        if paste_x + lw > image_width - 20:

            paste_x = (
                image_width
                - lw
                - 20
            )

        # Height safety
        if paste_y + lh > (
            y + max_height
        ):

            break

        if paste_y + lh > image_height:

            break

        # Paste handwritten line
        image.paste(
            line_image,
            (
                paste_x,
                paste_y
            ),
            line_image
        )

        # Ground-truth bounding box
        bbox = {
            "type": "text",
            "text": line,
            "bbox": [
                int(paste_x),
                int(paste_y),
                int(paste_x + lw),
                int(paste_y + lh)
            ],
            "line_index": line_index
        }

        bounding_boxes.append(
            bbox
        )

        # Natural line spacing variation
        current_y += (
            lh
            + line_spacing
            + random.randint(
                -2,
                3
            )
        )

    return image, bounding_boxes