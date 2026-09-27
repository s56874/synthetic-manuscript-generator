import random
import math

import numpy as np
import cv2

from PIL import Image, ImageFilter


# --------------------------------------------------
# Seed
# --------------------------------------------------

def set_seed(seed=42):

    random.seed(seed)
    np.random.seed(seed)


# --------------------------------------------------
# Rotate image + bounding boxes
# --------------------------------------------------

def rotate_image(
    image,
    annotations,
    max_angle=1.2
):

    angle = random.uniform(
        -max_angle,
        max_angle
    )

    width, height = image.size

    rotated = image.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=False,
        fillcolor=(185, 155, 110)
    )

    # Convert angle to radians
    theta = math.radians(
        -angle
    )

    cos_a = math.cos(theta)
    sin_a = math.sin(theta)

    cx = width / 2
    cy = height / 2

    new_annotations = []

    for ann in annotations:

        if "bbox" not in ann:
            new_annotations.append(ann)
            continue

        x1, y1, x2, y2 = ann["bbox"]

        corners = [
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2)
        ]

        transformed = []

        for x, y in corners:

            dx = x - cx
            dy = y - cy

            new_x = (
                cx
                + dx * cos_a
                - dy * sin_a
            )

            new_y = (
                cy
                + dx * sin_a
                + dy * cos_a
            )

            transformed.append(
                (new_x, new_y)
            )

        xs = [
            p[0]
            for p in transformed
        ]

        ys = [
            p[1]
            for p in transformed
        ]

        updated = ann.copy()

        updated["bbox"] = [
            max(0, int(min(xs))),
            max(0, int(min(ys))),
            min(width, int(max(xs))),
            min(height, int(max(ys)))
        ]

        new_annotations.append(
            updated
        )

    return rotated, new_annotations


# --------------------------------------------------
# Horizontal waviness
# --------------------------------------------------

def horizontal_waviness(
    image,
    amplitude=3.0,
    wavelength=250.0
):

    img = np.array(
        image
    )

    height, width = img.shape[:2]

    result = np.zeros_like(
        img
    )

    for y in range(height):

        shift = int(
            amplitude
            * math.sin(
                (2 * math.pi * y)
                / wavelength
            )
        )

        if shift > 0:

            result[y, shift:] = (
                img[y, :-shift]
            )

            result[y, :shift] = (
                img[y, 0]
            )

        elif shift < 0:

            shift_abs = abs(
                shift
            )

            result[y, :-shift_abs] = (
                img[y, shift_abs:]
            )

            result[y, -shift_abs:] = (
                img[y, -1]
            )

        else:

            result[y] = img[y]

    return Image.fromarray(
        result
    )


# --------------------------------------------------
# Vertical waviness
# --------------------------------------------------

def vertical_waviness(
    image,
    amplitude=2.0,
    wavelength=300.0
):

    img = np.array(
        image
    )

    height, width = img.shape[:2]

    result = np.zeros_like(
        img
    )

    for x in range(width):

        shift = int(
            amplitude
            * math.sin(
                (2 * math.pi * x)
                / wavelength
            )
        )

        if shift > 0:

            result[shift:, x] = (
                img[:-shift, x]
            )

            result[:shift, x] = (
                img[0, x]
            )

        elif shift < 0:

            shift_abs = abs(
                shift
            )

            result[:-shift_abs, x] = (
                img[shift_abs:, x]
            )

            result[-shift_abs:, x] = (
                img[-1, x]
            )

        else:

            result[:, x] = img[:, x]

    return Image.fromarray(
        result
    )


# --------------------------------------------------
# Page warp
# --------------------------------------------------

def page_warp(
    image,
    strength=2.0
):

    img = np.array(
        image
    )

    height, width = img.shape[:2]

    y_coords, x_coords = np.indices(
        (height, width),
        dtype=np.float32
    )

    displacement_x = (
        strength
        * np.sin(
            y_coords / 120.0
        )
    )

    displacement_y = (
        strength
        * np.sin(
            x_coords / 180.0
        )
    )

    map_x = (
        x_coords
        + displacement_x
    )

    map_y = (
        y_coords
        + displacement_y
    )

    warped = cv2.remap(
        img,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return Image.fromarray(
        warped
    )


# --------------------------------------------------
# Transform bounding box for page warp
# --------------------------------------------------

def warp_bbox(
    bbox,
    width,
    height,
    strength=2.0
):

    x1, y1, x2, y2 = bbox

    points = [
        (x1, y1),
        (x2, y1),
        (x2, y2),
        (x1, y2)
    ]

    transformed = []

    for x, y in points:

        dx = (
            strength
            * math.sin(
                y / 120.0
            )
        )

        dy = (
            strength
            * math.sin(
                x / 180.0
            )
        )

        new_x = x + dx
        new_y = y + dy

        transformed.append(
            (new_x, new_y)
        )

    xs = [
        p[0]
        for p in transformed
    ]

    ys = [
        p[1]
        for p in transformed
    ]

    return [
        max(0, int(min(xs))),
        max(0, int(min(ys))),
        min(width, int(max(xs))),
        min(height, int(max(ys)))
    ]


# --------------------------------------------------
# Local distortion
# --------------------------------------------------

def local_distortion(
    image,
    strength=1.5
):

    img = np.array(
        image
    )

    height, width = img.shape[:2]

    y_coords, x_coords = np.indices(
        (height, width),
        dtype=np.float32
    )

    wave_x = (
        strength
        * np.sin(
            y_coords / 70.0
        )
    )

    wave_y = (
        strength
        * np.sin(
            x_coords / 110.0
        )
    )

    map_x = (
        x_coords
        + wave_x
    )

    map_y = (
        y_coords
        + wave_y
    )

    result = cv2.remap(
        img,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return Image.fromarray(
        result
    )


# --------------------------------------------------
# Subtle blur
# --------------------------------------------------

def subtle_blur(
    image,
    min_radius=0.0,
    max_radius=0.45
):

    radius = random.uniform(
        min_radius,
        max_radius
    )

    if radius <= 0:

        return image

    return image.filter(
        ImageFilter.GaussianBlur(
            radius
        )
    )


# --------------------------------------------------
# Complete distortion
# --------------------------------------------------

def apply_distortion(
    image,
    annotations=None,
    rotation=True,
    waviness=True,
    page_warp_enabled=True,
    blur=True
):

    result = image.copy()

    if annotations is None:

        annotations = []

    updated_annotations = [
        ann.copy()
        for ann in annotations
    ]

    # ----------------------------------------------
    # Rotation
    # ----------------------------------------------

    if rotation:

        result, updated_annotations = rotate_image(
            result,
            updated_annotations,
            max_angle=0.8
        )

    # ----------------------------------------------
    # Waviness
    # ----------------------------------------------

    if waviness:

        result = horizontal_waviness(
            result,
            amplitude=2.0,
            wavelength=260.0
        )

        result = vertical_waviness(
            result,
            amplitude=1.2,
            wavelength=320.0
        )

    # ----------------------------------------------
    # Page warp
    # ----------------------------------------------

    if page_warp_enabled:

        warp_strength = 1.5

        result = page_warp(
            result,
            strength=warp_strength
        )

        width, height = result.size

        for ann in updated_annotations:

            if "bbox" not in ann:
                continue

            ann["bbox"] = warp_bbox(
                ann["bbox"],
                width,
                height,
                strength=warp_strength
            )

    # ----------------------------------------------
    # Local distortion
    # ----------------------------------------------

    if waviness:

        result = local_distortion(
            result,
            strength=0.8
        )

    # ----------------------------------------------
    # Final subtle blur
    # ----------------------------------------------

    if blur:

        result = subtle_blur(
            result,
            min_radius=0.0,
            max_radius=0.30
        )

    return result, updated_annotations