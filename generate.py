import os
import random
import json

from PIL import ImageDraw, ImageFont

from src.background import create_background
from src.text_data import prepare_script_samples
from src.text_renderer import render_text
from src.artifacts import apply_artifacts
from src.distortion import apply_distortion


# ============================================================
# SCRIPT CONFIGURATION
# ============================================================

SCRIPTS = {
    "devanagari": {
        "text_file": "texts/devanagari_md.md",
        "font_path": (
            "fonts/devanagari/"
            "NotoSansDevanagari-Regular.ttf.ttf"
        ),
        "seed": 42
    },

    "modi": {
        "text_file": "texts/Modi_md.md",
        "font_path": (
            "fonts/modi/"
            "NotoSansModi-Regular.ttf"
        ),
        "seed": 100
    },

    "sharada": {
        "text_file": "texts/sharada_md.md",
        "font_path": (
            "fonts/sharada/"
            "NotoSansSharada-Regular.ttf"
        ),
        "seed": 200
    }
}


# ============================================================
# DATASET SETTINGS
# ============================================================

IMAGE_WIDTH = 1600
IMAGE_HEIGHT = 1200

TOTAL_IMAGES = 100

TRAIN_COUNT = 85
VALIDATION_COUNT = 10
TEST_COUNT = 5


# ============================================================
# MANUSCRIPT GENERATOR
# ============================================================

class ManuscriptGenerator:

    def __init__(
        self,
        script_name,
        font_path,
        output_dir,
        width=1600,
        height=1200,
        seed=42
    ):

        self.script_name = script_name
        self.font_path = font_path
        self.output_dir = output_dir

        self.width = width
        self.height = height

        self.seed = seed

        os.makedirs(
            output_dir,
            exist_ok=True
        )

    # ========================================================
    # CREATE BACKGROUND
    # ========================================================

    def create_page(self):

        background_type = random.choice(
            [
                "aged_paper",
                "palm_leaf"
            ]
        )

        page = create_background(
            self.width,
            self.height,
            background_type=background_type
        )

        return page, background_type

    # ========================================================
    # MAIN TEXT
    # ========================================================

    def render_main_text(
        self,
        page,
        text,
        font_size,
        x,
        y,
        max_width,
        max_height,
        line_spacing
    ):

        page, boxes = render_text(
            page,
            text=text,
            font_path=self.font_path,
            font_size=font_size,
            x=x,
            y=y,
            max_width=max_width,
            max_height=max_height,
            line_spacing=line_spacing
        )

        return page, boxes

    # ========================================================
    # GET SMALL TEXT FROM SOURCE
    # ========================================================

    def get_source_fragment(self, source_text):

        words = source_text.split()

        if not words:
            return ""

        count = min(
            random.randint(2, 5),
            len(words)
        )

        return " ".join(
            words[:count]
        )

    # ========================================================
    # MARGINAL TEXT
    # ========================================================

    def add_marginal_text(
        self,
        page,
        source_text
    ):

        draw = ImageDraw.Draw(page)

        font_size = random.randint(
            22,
            30
        )

        font = ImageFont.truetype(
            self.font_path,
            font_size
        )

        marginal_text = self.get_source_fragment(
            source_text
        )

        if not marginal_text:
            return page, None

        if random.random() < 0.5:

            x = random.randint(
                30,
                70
            )

        else:

            x = random.randint(
                self.width - 180,
                self.width - 100
            )

        y = random.randint(
            200,
            850
        )

        ink = random.choice(
            [
                (75, 42, 25),
                (95, 48, 28),
                (110, 55, 30)
            ]
        )

        draw.text(
            (x, y),
            marginal_text,
            font=font,
            fill=ink
        )

        bbox = draw.textbbox(
            (x, y),
            marginal_text,
            font=font
        )

        annotation = {
            "type": "marginal_text",
            "text": marginal_text,
            "bbox": [
                int(bbox[0]),
                int(bbox[1]),
                int(bbox[2]),
                int(bbox[3])
            ]
        }

        return page, annotation

    # ========================================================
    # SECTION MARKER
    # ========================================================

    def add_section_marker(
        self,
        page
    ):

        draw = ImageDraw.Draw(page)

        size = random.randint(
            18,
            30
        )

        x = random.randint(
            55,
            100
        )

        y = random.randint(
            180,
            900
        )

        marker = random.choice(
            [
                "॥",
                "॰",
                "।"
            ]
        )

        font = ImageFont.truetype(
            self.font_path,
            size
        )

        draw.text(
            (x, y),
            marker,
            font=font,
            fill=(95, 45, 25)
        )

        bbox = draw.textbbox(
            (x, y),
            marker,
            font=font
        )

        annotation = {
            "type": "section_marker",
            "text": marker,
            "bbox": [
                int(bbox[0]),
                int(bbox[1]),
                int(bbox[2]),
                int(bbox[3])
            ]
        }

        return page, annotation

    # ========================================================
    # HIGHLIGHTED TEXT
    # ========================================================

    def add_highlight(
        self,
        page,
        source_text
    ):

        draw = ImageDraw.Draw(page)

        font_size = random.randint(
            26,
            36
        )

        font = ImageFont.truetype(
            self.font_path,
            font_size
        )

        words = source_text.split()

        if not words:
            return page, None

        text = random.choice(
            words
        )

        if len(text) > 20:

            text = text[:20]

        x = random.randint(
            400,
            1050
        )

        y = random.randint(
            850,
            1000
        )

        # Small highlight background
        text_bbox = draw.textbbox(
            (x, y),
            text,
            font=font
        )

        padding = 4

        draw.rectangle(
            (
                text_bbox[0] - padding,
                text_bbox[1] - padding,
                text_bbox[2] + padding,
                text_bbox[3] + padding
            ),
            fill=(175, 145, 90)
        )

        draw.text(
            (x, y),
            text,
            font=font,
            fill=(125, 48, 30)
        )

        bbox = draw.textbbox(
            (x, y),
            text,
            font=font
        )

        annotation = {
            "type": "highlighted_text",
            "text": text,
            "bbox": [
                int(bbox[0]),
                int(bbox[1]),
                int(bbox[2]),
                int(bbox[3])
            ]
        }

        return page, annotation

    # ========================================================
    # SAVE MARKDOWN ANNOTATION
    # ========================================================

    def save_markdown(
        self,
        md_path,
        image_name,
        background_type,
        font_size,
        source_text,
        annotations
    ):

        lines = []

        lines.append(
            f"# Annotation: {image_name}"
        )

        lines.append("")

        lines.append(
            f"- **Script:** {self.script_name}"
        )

        lines.append(
            f"- **Background:** {background_type}"
        )

        lines.append(
            f"- **Image Width:** {self.width}"
        )

        lines.append(
            f"- **Image Height:** {self.height}"
        )

        lines.append(
            f"- **Font Size:** {font_size}"
        )

        lines.append("")

        lines.append(
            "## Source Text"
        )

        lines.append("")

        lines.append(
            source_text
        )

        lines.append("")

        lines.append(
            "## Ground Truth Annotations"
        )

        lines.append("")

        if not annotations:

            lines.append(
                "No annotations."
            )

        else:

            for index, annotation in enumerate(
                annotations,
                start=1
            ):

                annotation_type = annotation.get(
                    "type",
                    "text"
                )

                text = annotation.get(
                    "text",
                    ""
                )

                bbox = annotation.get(
                    "bbox",
                    []
                )

                lines.append(
                    f"### Annotation {index}"
                )

                lines.append("")

                lines.append(
                    f"- **Type:** {annotation_type}"
                )

                lines.append(
                    f"- **Text:** {text}"
                )

                lines.append(
                    f"- **Bounding Box:** `{bbox}`"
                )

                lines.append("")

        with open(
            md_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n".join(lines)
            )

    # ========================================================
    # GENERATE ONE IMAGE
    # ========================================================

    def generate(
        self,
        text,
        image_id
    ):

        # Different random seed for each image
        image_seed = (
            self.seed +
            image_id * 1009
        )

        random.seed(
            image_seed
        )

        # ----------------------------------------------------
        # Background
        # ----------------------------------------------------

        page, background_type = (
            self.create_page()
        )

        annotations = []

        # ----------------------------------------------------
        # Split source text into two sections
        # ----------------------------------------------------

        words = text.split()

        split_point = len(words) // 2

        first_section = " ".join(
            words[:split_point]
        )

        second_section = " ".join(
            words[split_point:]
        )

        # ----------------------------------------------------
        # Main text settings
        # ----------------------------------------------------

        font_size = random.randint(
            40,
            46
        )

        # ----------------------------------------------------
        # First text block
        # ----------------------------------------------------

        first_x = random.randint(
            130,
            170
        )

        first_y = random.randint(
            130,
            180
        )

        first_width = random.randint(
            1200,
            1350
        )

        first_spacing = random.randint(
            18,
            30
        )

        page, boxes = self.render_main_text(
            page,
            first_section,
            font_size,
            first_x,
            first_y,
            first_width,
            500,
            first_spacing
        )

        annotations.extend(
            boxes
        )

        # ----------------------------------------------------
        # Second text block
        # ----------------------------------------------------

        second_x = random.randint(
            130,
            180
        )

        second_y = random.randint(
            640,
            700
        )

        second_width = random.randint(
            1200,
            1350
        )

        second_spacing = random.randint(
            18,
            30
        )

        page, boxes = self.render_main_text(
            page,
            second_section,
            font_size,
            second_x,
            second_y,
            second_width,
            350,
            second_spacing
        )

        annotations.extend(
            boxes
        )

        # ----------------------------------------------------
        # Marginal text
        # ----------------------------------------------------

        if random.random() < 0.75:

            page, annotation = (
                self.add_marginal_text(
                    page,
                    text
                )
            )

            if annotation:

                annotations.append(
                    annotation
                )

        # ----------------------------------------------------
        # Section marker
        # ----------------------------------------------------

        if random.random() < 0.80:

            page, annotation = (
                self.add_section_marker(
                    page
                )
            )

            if annotation:

                annotations.append(
                    annotation
                )

        # ----------------------------------------------------
        # Highlighted text
        # ----------------------------------------------------

        if random.random() < 0.55:

            page, annotation = (
                self.add_highlight(
                    page,
                    text
                )
            )

            if annotation:

                annotations.append(
                    annotation
                )

        # ----------------------------------------------------
        # Manuscript artifacts
        # ----------------------------------------------------

        page = apply_artifacts(
            page
        )

        # ----------------------------------------------------
        # Page distortion
        # ----------------------------------------------------

        page, annotations = apply_distortion(
            page,
            annotations=annotations,
            rotation=True,
            waviness=True,
            page_warp_enabled=True,
            blur=True
        )

        # ----------------------------------------------------
        # Image name
        # ----------------------------------------------------

        image_name = (
            f"{self.script_name}_"
            f"{image_id:04d}.png"
        )

        image_path = os.path.join(
            self.output_dir,
            image_name
        )

        # ----------------------------------------------------
        # Save image
        # ----------------------------------------------------

        page.save(
            image_path
        )

        # ----------------------------------------------------
        # JSON ground truth
        # ----------------------------------------------------

        annotation_data = {

            "image": image_name,

            "script": self.script_name,

            "background": background_type,

            "width": self.width,

            "height": self.height,

            "font_size": font_size,

            "source_text": text,

            "annotations": annotations
        }

        json_name = (
            f"{self.script_name}_"
            f"{image_id:04d}.json"
        )

        json_path = os.path.join(
            self.output_dir,
            json_name
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                annotation_data,
                file,
                ensure_ascii=False,
                indent=2
            )

        # ----------------------------------------------------
        # Markdown ground truth
        # ----------------------------------------------------

        md_name = (
            f"{self.script_name}_"
            f"{image_id:04d}.md"
        )

        md_path = os.path.join(
            self.output_dir,
            md_name
        )

        self.save_markdown(
            md_path=md_path,
            image_name=image_name,
            background_type=background_type,
            font_size=font_size,
            source_text=text,
            annotations=annotations
        )

        return (
            image_path,
            json_path,
            md_path
        )


# ============================================================
# GENERATE ONE SCRIPT DATASET
# ============================================================

def generate_script_dataset(
    script_name,
    config
):

    text_file = config[
        "text_file"
    ]

    font_path = config[
        "font_path"
    ]

    seed = config[
        "seed"
    ]

    print()
    print("=" * 70)

    print(
        f"{script_name.upper()} MANUSCRIPT DATASET"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Check text file
    # --------------------------------------------------------

    if not os.path.exists(
        text_file
    ):

        raise FileNotFoundError(
            f"Text file not found:\n{text_file}"
        )

    # --------------------------------------------------------
    # Check font
    # --------------------------------------------------------

    if not os.path.exists(
        font_path
    ):

        raise FileNotFoundError(
            f"Font not found:\n{font_path}"
        )

    print()

    print(
        "Text file :",
        text_file
    )

    print(
        "Font      :",
        font_path
    )

    # --------------------------------------------------------
    # Create 100 unique text samples
    # --------------------------------------------------------

    samples = prepare_script_samples(
        text_file,
        number_of_samples=100,
        seed=seed
    )

    if len(samples) != 100:

        raise RuntimeError(
            f"Expected 100 samples, "
            f"but got {len(samples)}."
        )

    print()

    print(
        f"100 unique {script_name} "
        "text samples created."
    )

    # --------------------------------------------------------
    # Dataset splits
    # --------------------------------------------------------

    splits = [
        ("train", 85),
        ("validation", 10),
        ("test", 5)
    ]

    sample_index = 0

    # --------------------------------------------------------
    # Generate each split
    # --------------------------------------------------------

    for split_name, split_count in splits:

        output_dir = os.path.join(
            "output",
            script_name,
            split_name
        )

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        print()
        print("-" * 70)

        print(
            f"Generating {split_name.upper()} "
            f"({split_count} images)"
        )

        print("-" * 70)

        generator = ManuscriptGenerator(
            script_name=script_name,
            font_path=font_path,
            output_dir=output_dir,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            seed=seed
        )

        for image_number in range(
            1,
            split_count + 1
        ):

            text = samples[
                sample_index
            ]

            # Number starts again from 0001
            # inside every split.
            image_id = image_number

            (
                image_path,
                json_path,
                md_path
            ) = generator.generate(
                text=text,
                image_id=image_id
            )

            print(
                f"[{image_number:03d}/"
                f"{split_count:03d}] "
                f"{os.path.basename(image_path)}"
            )

            sample_index += 1

    # --------------------------------------------------------
    # Completed
    # --------------------------------------------------------

    print()
    print("=" * 70)

    print(
        f"{script_name.upper()} DATASET "
        "GENERATION COMPLETED"
    )

    print("=" * 70)

    print()

    print(
        "Total images    : 100"
    )

    print(
        "Train           : 85"
    )

    print(
        "Validation      : 10"
    )

    print(
        "Test            : 5"
    )

    print(
        "Unique texts    : 100"
    )

    print(
        "Annotations     : PNG + MD + JSON"
    )

    print()


# ============================================================
# GENERATE ALL THREE DATASETS
# ============================================================

def main():

    print()
    print("=" * 70)
    print("SYNTHETIC MANUSCRIPT GENERATOR")
    print("=" * 70)

    print()

    print(
        "Devanagari : 100 images"
    )

    print(
        "Modi       : 100 images"
    )

    print(
        "Sharada    : 100 images"
    )

    print()

    print(
        "Total      : 300 images"
    )

    print()

    # --------------------------------------------------------
    # Generate all scripts
    # --------------------------------------------------------

    for script_name, config in SCRIPTS.items():

        generate_script_dataset(
            script_name,
            config
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("ALL DATASETS GENERATED SUCCESSFULLY")
    print("=" * 70)

    print()

    print(
        "Output folders:"
    )

    print(
        "output/devanagari/"
    )

    print(
        "output/modi/"
    )

    print(
        "output/sharada/"
    )

    print()

    print(
        "Each image has matching:"
    )

    print(
        "PNG + Markdown annotation + JSON ground truth"
    )

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()