import subprocess
import sys
import os
import argparse

# Define the virtual environment path relative to the script
VENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
PYTHON_EXECUTABLE = os.path.join(VENV_PATH, 'bin', 'python')
PIP_EXECUTABLE = os.path.join(VENV_PATH, 'bin', 'pip')

def setup_venv():
    """Checks for and sets up the virtual environment, installing dependencies."""
    if not os.path.exists(VENV_PATH):
        print(f"Creating virtual environment at {VENV_PATH}...")
        subprocess.check_call([sys.executable, '-m', 'venv', VENV_PATH])
        print("Virtual environment created.")

    print("Installing/updating dependencies...")
    # Install dependencies using the venv's pip
    subprocess.check_call([PIP_EXECUTABLE, 'install', 'google-cloud-aiplatform', 'Pillow'])
    print("Dependencies installed.")

def run_image_generation_logic(prompt: str, output_file: str):
    """Runs the core image generation logic."""
    # This part will be executed by the python in the venv
    script_content = f"""
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import os

# Initialize Vertex AI
# It will use GOOGLE_APPLICATION_CREDENTIALS or gcloud config
vertexai.init()

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

images = model.generate_images(
    prompt=\"{prompt}\",
    number_of_images=1,
    seed=1,
    add_watermark=False,
)

images[0].save(location=\"{output_file}\")
print(f"Image saved to {output_file}")
"""
    # Write this logic to a temporary file
    temp_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_image_gen_logic.py')
    with open(temp_script_path, 'w') as f:
        f.write(script_content)

    # Execute the temporary file using the venv's python
    subprocess.check_call([PYTHON_EXECUTABLE, temp_script_path])

    # Clean up temporary file
    os.remove(temp_script_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an image using Google Cloud Vertex AI Imagen.")
    parser.add_argument("--prompt", required=True, help="The text description for image generation.")
    parser.add_argument("--filename", required=True, help="The desired output filename for the image.")

    args = parser.parse_args()

    # Ensure venv and dependencies are set up
    setup_venv()

    # Run the core logic within the venv
    run_image_generation_logic(args.prompt, args.filename)
