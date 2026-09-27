import re
import random
import hashlib


# ---------------------------------------------------------
# Read source manuscript file
# ---------------------------------------------------------

def read_source_file(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    return text


# ---------------------------------------------------------
# Clean Markdown
# ---------------------------------------------------------

def clean_markdown(text):

    # Remove code blocks
    text = re.sub(
        r"```.*?```",
        " ",
        text,
        flags=re.DOTALL
    )

    # Remove Markdown headings
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Convert Markdown links to their text
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    # Remove HTML tags
    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    # Remove Markdown formatting
    text = re.sub(
        r"[*_`~]+",
        "",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


# ---------------------------------------------------------
# Split source into paragraphs
# ---------------------------------------------------------

def split_into_paragraphs(text):

    paragraphs = []

    for block in text.split("\n"):

        block = block.strip()

        if len(block) >= 80:

            paragraphs.append(block)

    return paragraphs


# ---------------------------------------------------------
# Create UNIQUE text samples
# ---------------------------------------------------------

def create_text_samples(
    source_text,
    number_of_samples=100,
    min_words=100,
    max_words=180,
    seed=42
):

    random.seed(seed)

    paragraphs = split_into_paragraphs(
        source_text
    )

    if not paragraphs:

        raise ValueError(
            "No usable text found in source corpus."
        )

    # -----------------------------------------------------
    # Convert paragraphs into word lists
    # -----------------------------------------------------

    word_blocks = []

    for paragraph in paragraphs:

        words = paragraph.split()

        if len(words) >= min_words:

            word_blocks.append(words)

    if not word_blocks:

        raise ValueError(
            "Source corpus does not contain enough "
            "usable text."
        )

    # -----------------------------------------------------
    # Generate samples
    # -----------------------------------------------------

    samples = []

    used_hashes = set()

    attempts = 0

    max_attempts = number_of_samples * 300

    while len(samples) < number_of_samples:

        attempts += 1

        if attempts > max_attempts:

            raise RuntimeError(
                f"Could create only "
                f"{len(samples)} unique samples "
                f"from the supplied corpus."
            )

        # Random paragraph
        words = random.choice(
            word_blocks
        )

        # Random sample length
        upper_limit = min(
            max_words,
            len(words)
        )

        if upper_limit < min_words:

            continue

        sample_length = random.randint(
            min_words,
            upper_limit
        )

        # Random starting point
        max_start = (
            len(words) -
            sample_length
        )

        if max_start > 0:

            start = random.randint(
                0,
                max_start
            )

        else:

            start = 0

        selected_words = words[
            start:start + sample_length
        ]

        sample = " ".join(
            selected_words
        ).strip()

        # Ignore very short samples
        if len(sample) < 150:

            continue

        # -------------------------------------------------
        # Hash-based uniqueness check
        # -------------------------------------------------

        sample_hash = hashlib.sha256(
            sample.encode("utf-8")
        ).hexdigest()

        if sample_hash in used_hashes:

            continue

        used_hashes.add(
            sample_hash
        )

        samples.append(
            sample
        )

    return samples


# ---------------------------------------------------------
# Main function
# ---------------------------------------------------------

def prepare_script_samples(
    file_path,
    number_of_samples=100,
    seed=42
):

    print(
        f"Reading: {file_path}"
    )

    raw_text = read_source_file(
        file_path
    )

    print(
        f"Raw characters: {len(raw_text):,}"
    )

    cleaned_text = clean_markdown(
        raw_text
    )

    print(
        f"Clean characters: {len(cleaned_text):,}"
    )

    samples = create_text_samples(
        cleaned_text,
        number_of_samples=number_of_samples,
        min_words=100,
        max_words=180,
        seed=seed
    )

    print(
        f"Unique samples created: {len(samples)}"
    )

    return samples