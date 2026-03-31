
import os
import re
from google.cloud import texttospeech

# Set the environment variable for Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ubuntu/.openclaw/workspace/.env.d/google-sa.json"

def convert_to_ssml(text):
    """
    Converts plain text with custom pause markers "(停 X 秒)" to SSML format.
    """
    # Replace "(停 X 秒)" with <break time="Xs"/>
    ssml_text = re.sub(r'\(停 (\d+) 秒\)', r'<break time="\1s"/>', text)
    return f'<speak>{ssml_text}</speak>'

def synthesize_text(text, output_filename="output.mp3"):
    """
    Synthesizes speech from the input text and saves it as an MP3 file.
    Assumes the input text might contain custom pause markers.
    """
    client = texttospeech.TextToSpeechClient()

    ssml_text = convert_to_ssml(text)

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Select the voice parameters (e.g., languageCode, ssmlGender)
    # You can customize these as needed.
    voice = texttospeech.VoiceSelectionParams(
        language_code="zh-TW",
        name="cmn-TW-Wavenet-A",  # Natural female voice for zh-TW (Mandarin, Taiwan)
    )

    # Select the audio file type and speaking rate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9, # 0.9x speed
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # input_text = "你好，這是一段測試。 (停 2 秒) 測試結束。"
    # synthesize_text(input_text, "test_output.mp3")
    print("Script generate_tts.py created. Please uncomment the example usage or call synthesize_text function.")
