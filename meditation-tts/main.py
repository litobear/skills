
import os
import subprocess
import sys
import argparse

# Define paths relative to the skill directory
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(SKILL_DIR, "tts_venv")
PYTHON_EXEC = os.path.join(VENV_DIR, "bin", "python3") # Use python3 for clarity
PIP_EXEC = os.path.join(VENV_DIR, "bin", "pip3") # Use pip3 for clarity

# Ensure the scripts directory is on the path for generate_tts.py
# Note: In a production setting, generate_tts.py would ideally be a proper module
# and its functions imported directly, or its functionality integrated here.
# For now, we will create a temporary runner script to execute it via venv.

def setup_venv():
    """Ensures the virtual environment is set up and dependencies are installed."""
    if not os.path.exists(VENV_DIR):
        print(f"Creating virtual environment at {VENV_DIR}...")
        try:
            subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True, capture_output=True, text=True)
            print("Virtual environment created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating venv: {e.stderr}")
            sys.exit(1)

    print("Installing google-cloud-texttospeech in venv...")
    try:
        # Use --no-warn-script-location to suppress warnings about scripts not being on PATH
        subprocess.run([PIP_EXEC, "install", "google-cloud-texttospeech", "--no-warn-script-location"], check=True, capture_output=True, text=True)
        print("Dependencies installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e.stderr}")
        sys.exit(1)

def run_tts_in_venv(input_text, output_filename):
    """Runs the TTS generation using the venv's Python."""
    # Create a temporary runner script to execute generate_tts.py
    temp_script_path = os.path.join(SKILL_DIR, "temp_tts_runner.py")
    
    # Escape single quotes in input_text for the f-string
    escaped_input_text = input_text.replace("'", "\'")

    with open(temp_script_path, "w") as f:
        f.write(f"""
import os
import sys
# Add the directory containing generate_tts.py to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from generate_tts import synthesize_text

# Set the environment variable for Google Application Credentials within this process
# This path is relative to the OpenClaw workspace, which is the current working directory for skills
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ubuntu/.openclaw/workspace/.env.d/google-sa.json"

input_text = '{escaped_input_text}'
output_filename = '{output_filename}'

synthesize_text(input_text, output_filename)
""")

    print(f"Generating audio to {output_filename}...")
    try:
        subprocess.run([PYTHON_EXEC, temp_script_path], check=True, capture_output=True, text=True)
        print(f"Audio content written to file \"{output_filename}\"")
    except subprocess.CalledProcessError as e:
        print(f"Error during TTS generation: {e.stderr}")
        sys.exit(1)
    finally:
        # Clean up temp script
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate TTS audio with SSML for meditation skill.")
    parser.add_argument("--text", required=True, help="Input text for TTS (can be SSML).")
    parser.add_argument("--output", default=os.path.join(os.getcwd(), "meditation_audio.mp3"), help="Output audio filename (defaults to current working directory).")
    args = parser.parse_args()

    setup_venv()
    run_tts_in_venv(args.text, args.output)

