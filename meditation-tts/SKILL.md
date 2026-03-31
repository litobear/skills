
---

🧘 Meditation TTS Skill (Google Cloud TTS)

Overview

This skill transforms user input into natural, human-like meditation voice output using:

LLM → generate SSML (Speech Synthesis Markup Language)

Google Cloud Text-to-Speech → synthesize audio


Goal:

> Produce calm, yoga-teacher-style guided speech with natural breathing rhythm.




---


---

Usage

This skill can be invoked via its `main.py` script. It automatically manages its Python virtual environment (venv) and installs necessary dependencies (`google-cloud-texttospeech`).

**To generate audio:**

```bash
/usr/bin/python3 /home/ubuntu/.openclaw/workspace/skills/meditation-tts/main.py --text "<YOUR_TEXT_OR_SSML>" [--output <OUTPUT_FILENAME>]
```

**Arguments:**

*   `--text` (required): The input text or SSML string to convert to speech.
*   `--output` (optional): The name of the output MP3 file. Defaults to `meditation_audio.mp3` in the current working directory.

**Example:**

```bash
/usr/bin/python3 /home/ubuntu/.openclaw/workspace/skills/meditation-tts/main.py --text "請慢慢吸氣<break time='1s'/>然後吐氣<break time='1.5s'/>放鬆身體" --output "my_meditation.mp3"
```

---

Architecture

User Input
   ↓
LLM (SSML Generator)
   ↓
Google Cloud TTS API
   ↓
Audio (MP3 / Stream)

Key Principle

LLM controls how to speak

TTS handles voice rendering only



---

Skill Prompt (Core)

You are a meditation voice script generator.

Your job is to convert any instruction into calm, natural SSML for Google Cloud TTS.

STYLE:
- Like a yoga / meditation teacher
- Slow, gentle, warm
- With breathing rhythm

RULES:
1. Always output valid SSML wrapped in <speak>
2. Use <prosody rate="0.75~0.9" pitch="-2st~-4st">
3. Break sentences into short phrases
4. Add breathing pauses using <break time="1s~3s">
5. Add longer pauses after important sentences
6. Use soft guiding tone (not commands, but invitations)
7. Occasionally add emphasis using <emphasis level="moderate">
8. Avoid long continuous text
9. Insert natural rhythm: phrase → pause → phrase

BREATHING PATTERN:
- inhale → 2s pause
- exhale → 2~3s pause

OUTPUT:
Only SSML. No explanation. If possible, save this xml file.


---

SSML Template (Base Pattern)

<speak>
  <prosody rate="0.8" pitch="-3st">

    歡迎你來到這段放鬆練習
    <break time="2s"/>

    現在
    <break time="1s"/>
    請輕輕閉上眼睛
    <break time="2s"/>

    慢慢吸氣
    <break time="2s"/>

    再慢慢吐氣
    <break time="3s"/>

    讓身體自然放鬆
    <break time="3s"/>

  </prosody>
</speak>


---

Voice Configuration

Recommended Voices (Traditional Chinese)

cmn-TW-Neural2-A

cmn-TW-Neural2-B


Premium (if enabled)

Studio voices (more human-like)



---

Audio Config

{
  "audioConfig": {
    "audioEncoding": "MP3",
    "speakingRate": 0.85,
    "pitch": -3,
    "volumeGainDb": 2
  }
}

Notes

speakingRate < 1 → calmer tone

lower pitch → warmer, less robotic



---

Example Output

Input

帶我做一段放鬆練習

LLM Output (SSML)

<speak>
  <prosody rate="0.8" pitch="-3st">

    現在
    <break time="1s"/>
    讓我們一起進入一段放鬆的時間
    <break time="2s"/>

    請慢慢吸氣
    <break time="2s"/>

    感受空氣進入你的身體
    <break time="2s"/>

    然後
    <break time="0.5s"/>
    緩緩吐氣
    <break time="3s"/>

    讓肩膀慢慢放鬆
    <break time="2s"/>

    讓所有的緊繃
    <break time="1s"/>
    一點一點釋放
    <break time="3s"/>

  </prosody>
</speak>


---

Advanced Optimization

1. Randomized Timing (Reduce Robotic Feel)

Vary <break> duration:

1.5s / 2s / 2.5s


Slight variation in phrasing



---

2. Modes

Mode	Rate	Break	Use Case

Relax	0.85	1–2s	日常放鬆
Focus	0.9	0.5–1s	專注引導
Sleep	0.75	2–4s	入睡 / 冥想



---

3. Background Audio (Recommended)

To reach production quality:

Add post-processing:

white noise

ocean waves

ambient music



---

4. Chunking Strategy (重要)

Avoid long SSML:

Split into segments:
- 20–40 seconds per chunk
- stream or concatenate


---

Common Mistakes

❌ No SSML
❌ Long sentences
❌ No pauses
❌ Default voice
❌ speakingRate = 1.0
❌ No emotional tone


---

Production Checklist

[ ] SSML generation enabled

[ ] Correct voice selected

[ ] speakingRate tuned

[ ] Break timing present

[ ] Chunking implemented

[ ] Optional background audio



---

Future Enhancements

Streaming TTS

Emotion-aware SSML

Dynamic breathing pacing

Multi-language support

Personalized voice profiles



---

Summary

> High-quality meditation audio is not about TTS engine quality.
It is about SSML structure + rhythm design + voice tuning.




---




