import os
from gtts import gTTS
import pyttsx3
from playsound import playsound
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import requests


class TextToSpeech:
    def __init__(self, elevenlabs_api_key=None):
        self.elevenlabs_api_key = elevenlabs_api_key

    def convert_with_elevenlabs(self, text, output_filename=None):  # data/audios/output_voice.wav
        if not self.elevenlabs_api_key:
            raise ValueError("API key for ElevenLabs is not set.")

        client = ElevenLabs(api_key=self.elevenlabs_api_key)

        audio = client.text_to_speech.convert(
            voice_id="cgSgspJ2msm6clMCkdW9",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_flash_v2_5",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=False,
            ),
        )

        audio_bytes = b''.join(audio)

        with open(output_filename, 'wb') as f:
            f.write(audio_bytes)

        playsound(output_filename)
        os.remove(output_filename)

    def convert_with_gtts(self, text,  output_filename=None):  # data/audios/output_voice.wav

        tts = gTTS(text=text, lang='pt', slow=False)
        tts.save(output_filename)
        os.system(f"start {output_filename}")

    def convert_with_pyttsx3(self, text):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)

            print(f"KaLLia: {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Erro ao converter texto para áudio com pyttsx3: {e}")

    def convert_with_voicevox(self, text, speaker_id=1):
        try:
            params = {"text": text, "speaker": speaker_id}

            synthesis_response = requests.post("http://127.0.0.1:50021/audio_query", params=params)
            synthesis_response.raise_for_status()
            audio_query = synthesis_response.json()

            synthesis_audio = requests.post(
                "http://127.0.0.1:50021/synthesis",
                json=audio_query,
                params={"speaker": speaker_id}
            )
            synthesis_audio.raise_for_status()

            with open('data/audios/output_voice.wav', "wb") as f:
                f.write(synthesis_audio.content)
        except Exception as e:
            print(f"Erro ao converter texto para áudio com VoiceVox: {e}")