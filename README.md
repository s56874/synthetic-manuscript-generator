# Synthetic Manuscript Generator

A Python pipeline that generates synthetic historical manuscript images from raw text.

Supported scripts:

- Devanagari
- Modi
- Sharada

## Features

- Palm-leaf and aged-paper backgrounds
- Manuscript textures and aging effects
- Main text and multiple text blocks
- Marginal and side text
- Section and punctuation markers
- Highlighted text
- Ink color variation and fading
- Smudges, stains, folds and page warping
- Markdown and JSON annotations

## Dataset

The project generates **100 images per script**:

| Script | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| Devanagari | 85 | 10 | 5 | 100 |
| Modi | 85 | 10 | 5 | 100 |
| Sharada | 85 | 10 | 5 | 100 |
| **Total** | **255** | **30** | **15** | **300** |

Each image has corresponding `.md` and `.json` annotation files.

## Project Structure

```text
synthetic-manuscript-generator/
│
├── generate.py
├── config.yaml
├── requirements.txt
├── README.md
│
├── fonts/
├── texts/
├── src/
└── output/
```

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run:

```bash
python generate.py
```

The generated dataset is saved in the `output/` folder.

## Configuration

All main settings can be changed in:

```text
config.yaml
```

You can configure image size, number of images, splits, fonts, text files, margins, and manuscript effects.

## Hugging Face Dataset

**Dataset:** SamarthKokate55/synthetic-manuscript-generator

**Link:** 'https://huggingface.co/datasets/SamarthKokate55/synthetic-manuscript-generator'

The dataset contains Devanagari, Modi, and Sharada images with train, validation, and test splits.

## Technologies

- Python
- Pillow
- OpenCV
- NumPy
- SciPy
- PyYAML
- Hugging Face Datasets

## Purpose

This dataset can be used for research and development in:

- Indic script recognition
- OCR
- Handwritten text recognition
- Document image analysis
- Computer vision

## Author

**Samarth Kokate**

B.Tech Computer Science Engineering (Data Science)