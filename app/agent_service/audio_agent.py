from google.cloud import texttospeech
import os

class AudioAgent:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def emotional_tts(self, text, speaking_rate=1.0, pitch=0.0, path="output.wav"):
        input_text = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-F",  # More natural voice
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # WAV format
            speaking_rate=speaking_rate,
            pitch=pitch
        )

        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        # Ensure .wav file extension
        if not path.endswith('.wav'):
            path += '.wav'

        with open(path, "wb") as out:
            out.write(response.audio_content)
            print(f'🎧 Audio content written to {path}')

    def run(self, script_result):
        for i, script in enumerate(script_result['top'][:2]):
            text = f"{script['title']}. {script['body']}."
            fname = f"{script['month']}_{script['age_group']}_{script['region']}_top_{i}"
            path = f"assets/{script_result['bucket_id']}/top/{fname}.wav"
            # Only if the the image exists 
            if os.path.exists(f"assets/{script_result['bucket_id']}/top/{fname}.png"):
                self.emotional_tts(text, path=path)

        for i, script in enumerate(script_result['bottom'][:2]):
            text = f"{script['title']}. {script['body']}."
            fname = f"{script['month']}_{script['age_group']}_{script['region']}_bottom_{i}"
            path = f"assets/{script_result['bucket_id']}/bottom/{fname}.wav"
            if os.path.exists(f"assets/{script_result['bucket_id']}/bottom/{fname}.png"):
                self.emotional_tts(text, path=path)

        return script_result
    

AUDIO_AGENT = AudioAgent()