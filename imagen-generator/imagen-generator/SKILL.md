---
name: imagen-generator
description: Generates images from text prompts using Google Cloud Vertex AI Imagen 3.0 model. Use when the user asks to create an image, generate an image, or explicitly mentions Imagen, Vertex AI for image generation. Requires Google Service Account authorization on the system.
---

# Imagen Generator

## Overview
This skill enables the generation of images from text prompts using Google Cloud's Vertex AI Imagen 3.0 model. It leverages the system's configured Google Service Account for authentication.

## How to Use
To generate an image, call the `generate_image.py` script with your desired prompt and an output filename. The script will automatically handle the setup of a virtual environment and installation of necessary Python dependencies (`google-cloud-aiplatform` and `Pillow`).

### 1. Generate an Image
Use the `generate_image.py` script located in the `scripts/` directory.

```bash
/path/to/skill/scripts/generate_image.py --prompt "your image description" --filename "output.jpeg"
```

**Arguments:**
*   `--prompt`: The text description of the image you want to generate.
*   `--filename`: The name of the output image file (e.g., `my_image.jpeg`).

**Example:**
```bash
/home/ubuntu/.openclaw/workspace/skills/public/imagen-generator/scripts/generate_image.py --prompt "a rabbit jumping high" --filename "rabbit_jumping.jpeg"
```

## Requirements
*   **Google Cloud Project:** An active Google Cloud project.
*   **Vertex AI API Enabled:** Ensure the Vertex AI API is enabled in your Google Cloud project.
*   **Google Service Account Authorization:** The system must be configured with a Google Service Account that has the necessary permissions to use Vertex AI. This is typically done by setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file.

## Resources
### `scripts/`
*   `generate_image.py`: The Python script responsible for calling the Vertex AI Imagen 3.0 model and generating the image. This script manages its own Python virtual environment and dependencies.
