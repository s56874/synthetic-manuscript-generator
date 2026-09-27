import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def read_text():
    """
    Read the source manuscript text.
    """

    with open(TEXT_PATH, "r", encoding="utf-8") as file:
        text = file.read()

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def create_annotation(image_name, text, split):
    """
    Create one JSON annotation for an image.
    """

    annotation = {
        "image": image_name,
        "script": "devanagari",
        "split": split,
        "text": text
    }

    return annotation


def save_annotation(split, image_number, text):
    """
    Save annotation as JSON.
    """

    split_dir = os.path.join(
        OUTPUT_DIR,
        split
    )

    os.makedirs(split_dir, exist_ok=True)

    image_name = f"devanagari_{image_number:03d}.png"
    annotation_name = f"devanagari_{image_number:03d}.json"

    annotation = create_annotation(
        image_name,
        text,
        split
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

    print("Created:", annotation_path)


def create_annotations():
    """
    Create annotations for:
    85 train
    10 validation
    5 test
    """

    text = read_text()

    print("Source text loaded.")
    print("Characters:", len(text))

    # Training annotations
    for i in range(1, 86):
        save_annotation(
            "train",
            i,
            text
        )

    # Validation annotations
    for i in range(86, 96):
        save_annotation(
            "validation",
            i,
            text
        )

    # Test annotations
    for i in range(96, 101):
        save_annotation(
            "test",
            i,
            text
        )

    print()
    print("================================")
    print("Annotation generation completed!")
    print("Train      : 85")
    print("Validation : 10")
    print("Test       : 5")
    print("Total      : 100")
    print("================================")


if __name__ == "__main__":
    create_annotations()